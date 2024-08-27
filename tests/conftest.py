import os
import pytest
import pytest_asyncio
import warnings

from uuid import uuid4

from pytest_nhsd_apim.identity_service import (
    AuthorizationCodeConfig,
    AuthorizationCodeAuthenticator,
    ClientCredentialsConfig,
    ClientCredentialsAuthenticator,
)
from pytest_nhsd_apim.apigee_apis import (
    ApiProductsAPI,
    ApigeeClient,
    ApigeeNonProdCredentials,
    DeveloperAppsAPI,
)


from data import Actor


def _create_apigee_client():
    config = ApigeeNonProdCredentials()
    return ApigeeClient(config=config)


def get_env(variable_name: str) -> str:
    """Returns an environment variable"""
    try:
        var = os.environ[variable_name]
        if not var:
            raise RuntimeError(f"Variable is null, Check {variable_name}.")
        return var
    except KeyError:
        raise RuntimeError(f"Variable is not set, Check {variable_name}.")


@pytest.fixture(scope="session")
def environment():
    return get_env("ENVIRONMENT")


@pytest.fixture(scope="session")
def service_name():
    return get_env("FULLY_QUALIFIED_SERVICE_NAME")


@pytest.fixture(scope="session")
def service_base_path():
    return get_env("SERVICE_BASE_PATH")


@pytest.fixture(scope="session")
def service_url(environment, service_base_path):
    if environment == "prod":
        base_url = "https://api.service.nhs.uk"
    else:
        base_url = f"https://{environment}.api.service.nhs.uk"

    return f"{base_url}/{service_base_path}"


@pytest.fixture(scope="session")
def is_mocked_environment(environment, service_base_path):
    return environment == "internal-dev" and "ft" in service_base_path


@pytest.fixture(scope="session")
def status_endpoint_api_key():
    return get_env("STATUS_ENDPOINT_API_KEY")


@pytest.fixture(scope="session")
def asid(is_mocked_environment):
    return (
        get_env("ERS_MOCK_ASID") if is_mocked_environment else get_env("ERS_TEST_ASID")
    )


@pytest.fixture(scope="session")
def referring_clinician(is_mocked_environment):
    return Actor.RC_DEV if is_mocked_environment else Actor.RC


@pytest.fixture(scope="session")
def referring_clinician_insufficient_ial():
    return Actor.RC_INSUFFICIENT_IAL


@pytest.fixture(scope="session")
def oauth_url():
    oauth_proxy = get_env("OAUTH_PROXY")
    oauth_base_uri = get_env("OAUTH_BASE_URI")
    return f"{oauth_base_uri}/{oauth_proxy}"


@pytest.fixture(scope="session")
def app_restricted_ods_code(is_mocked_environment):
    return "R68" if is_mocked_environment else "RCD"


@pytest.fixture(scope="session")
def app_restricted_user_id(is_mocked_environment):
    return "000000000101" if is_mocked_environment else "555032000100"


@pytest.fixture(
    scope="session",
    params=["PROVIDER_AUTHORISED_APPLICATION", "REFERRER_AUTHORISED_APPLICATION"],
)
def app_restricted_business_function(request):
    return request.param


@pytest.fixture()
def client():
    return _create_apigee_client()


@pytest_asyncio.fixture
async def user_restricted_product(client, make_product):
    # Setup
    productName = await make_product(
        ["urn:nhsd:apim:user-nhs-id:aal3:e-referrals-service-api"]
    )

    print(f"product created: {productName}")
    yield productName

    # Teardown
    print(f"Cleanup product: {productName}")
    product = ApiProductsAPI(client=client)
    product.delete_product_by_name(product_name=productName)


@pytest.fixture
def make_product(client, environment, service_name):
    async def _make_product(product_scopes):
        product = ApiProductsAPI(client=client)

        proxies = [f"identity-service-mock-{environment}"]

        if service_name is not None:
            proxies.append(service_name)

        product_name = f"apim-auto-{uuid4()}"
        attributes = [
            {"name": "access", "value": "public"},
            {"name": "ratelimit", "value": "10ps"},
        ]
        body = {
            "proxies": proxies,
            "scopes": product_scopes,
            "name": product_name,
            "displayName": product_name,
            "attributes": attributes,
            "approvalType": "auto",
            "environments": ["internal-dev"],
            "quota": 500,
            "quotaInterval": "1",
            "quotaTimeUnit": "minute",
        }
        product.post_products(body=body)
        return product_name

    return _make_product


@pytest_asyncio.fixture
async def user_restricted_app(client, make_app, user_restricted_product, asid):
    # Setup
    app = await make_app(user_restricted_product, {"asid": asid})

    appName = app["name"]
    print(f"App created: {appName}")
    yield app

    # Teardown
    print(f"Cleanup app: {appName}")
    app = DeveloperAppsAPI(client=client)
    app.delete_app_by_name(email="apm-testing-internal-dev@nhs.net", app_name=appName)


@pytest.fixture
def make_app(client):
    async def _make_app(product, custom_attributes={}):
        # Setup
        devAppAPI = DeveloperAppsAPI(client=client)
        app_name = f"apim-auto-{uuid4()}"

        attributes = [
            {"name": key, "value": value} for key, value in custom_attributes.items()
        ]
        attributes.append({"name": "DisplayName", "value": app_name})

        body = {
            "apiProducts": [product],
            "attributes": attributes,
            "name": app_name,
            "scopes": [],
            "status": "approved",
            "callbackUrl": "http://example.com",
        }

        app = devAppAPI.create_app(email="apm-testing-internal-dev@nhs.net", body=body)
        print(f"CREATED APP NAME: {app_name}")

        return app

    return _make_app


@pytest.fixture
def authenticate_user(client, user_restricted_app, environment, oauth_url):
    async def _auth(actor: Actor):
        print(f"Attempting to authenticate: {actor}")

        credentials = user_restricted_app["credentials"][0]

        config = AuthorizationCodeConfig(
            environment=environment,
            identity_service_base_url=oauth_url,
            client_id=credentials["consumerKey"],
            client_secret=credentials["consumerSecret"],
            scope="nhs-cis2",
            login_form={"username": actor.user_id},
            callback_url=user_restricted_app["callbackUrl"],
        )
        # 2. Pass the config to the Authenticator
        authenticator = AuthorizationCodeAuthenticator(config=config)

        # 3. Get your token
        token_response = authenticator.get_token()
        print(f"user restricted resp: {token_response}")
        return token_response["access_token"]

    return _auth


@pytest_asyncio.fixture
async def app_restricted_product(client, make_product):
    # Setup
    productName = await make_product(
        ["urn:nhsd:apim:app:level3:e-referrals-service-api"]
    )

    print(f"product created: {productName}")
    yield productName

    # Teardown
    print(f"Cleanup product: {productName}")
    product = ApiProductsAPI(client=client)
    product.delete_product_by_name(product_name=productName)


@pytest_asyncio.fixture
async def app_restricted_app(
    client,
    jwt_public_key_url,
    make_app,
    app_restricted_product,
    asid,
    app_restricted_ods_code,
    app_restricted_user_id,
    app_restricted_business_function,
):
    # Setup
    app = await make_app(
        app_restricted_product,
        {
            "asid": asid,
            "app-restricted-ods-code": app_restricted_ods_code,
            "app-restricted-user-id": app_restricted_user_id,
            "app-restricted-business-function": app_restricted_business_function,
            "jwks-resource-url": jwt_public_key_url,
        },
    )
    appName = app["name"]
    print(f"App created: {appName}")

    yield app

    # Teardown
    print(f"Cleanup app: {appName}")
    app = DeveloperAppsAPI(client=client)
    app.delete_app_by_name(email="apm-testing-internal-dev@nhs.net", app_name=appName)


@pytest.fixture
def app_restricted_access_code(
    client, app_restricted_app, jwt_private_key_pem, environment, oauth_url
):
    credentials = app_restricted_app["credentials"][0]

    config = ClientCredentialsConfig(
        environment=environment,
        identity_service_base_url=oauth_url,
        client_id=credentials["consumerKey"],
        jwt_private_key=jwt_private_key_pem,
        jwt_kid="test-1",
    )
    # 2. Pass the config to the Authenticator
    authenticator = ClientCredentialsAuthenticator(config=config)

    # 3. Get your token
    token_response = authenticator.get_token()
    assert "access_token" in token_response
    return token_response["access_token"]


@pytest.fixture(scope="session")
def _create_test_app(
    _create_test_app,
    asid,
):
    """
    This fixture is overriding a private fixture housed within the pytest_nhsd_apim module to update any created app with the ASID currently being utilised.
    This is required as the private fixture does not publicise the attributes it associates with any created application, so instead we need to modify the created application to
    append the ASID required.
    """

    warnings.warn("invoking custom create test app.")

    created_app = _create_test_app
    warnings.warn(f"created app={created_app}")

    api = DeveloperAppsAPI(client=_create_apigee_client())

    # Update the attributes of the created application to add in the ASID attribute.
    modified_attributes = created_app["attributes"] + [{"key": "asid", "value": asid}]

    created_app["attributes"] = modified_attributes

    warnings.warn(f"updated app={created_app}")

    return api.put_app_by_name(
        email="apm-testing-internal-dev@nhs.net",
        app_name=created_app["name"],
        body=created_app,
    )
