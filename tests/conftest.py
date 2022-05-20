import os

from uuid import uuid4
from time import time

import pytest
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps
from api_test_utils.apigee_api_products import ApigeeApiProducts
from api_test_utils.oauth_helper import OauthHelper

__JWKS_RESOURCE_URL = "https://raw.githubusercontent.com/NHSDigital/identity-service-jwks/main/jwks/internal-dev/9baed6f4-1361-4a8e-8531-1f8426e3aba8.json"


def get_env(variable_name: str) -> str:
    """Returns an environment variable"""
    try:
        var = os.environ[variable_name]
        if not var:
            raise RuntimeError(f"Variable is null, Check {variable_name}.")
        return var
    except KeyError:
        raise RuntimeError(f"Variable is not set, Check {variable_name}.")


def get_env_file(variable_name: str) -> str:
    """Returns an environment variable as path"""
    try:
        path = os.path.abspath(os.environ[variable_name])
        if not path:
            raise RuntimeError(f"Variable is null, Check {variable_name}.")
        with open(path, "r") as f:
            contents = f.read()
        if not contents:
            raise RuntimeError(f"Contents of file empty. Check {variable_name}.")
        return contents
    except KeyError:
        raise RuntimeError(f"Variable is not set, Check {variable_name}.")


@pytest.fixture(scope="session")
def environment():
    return get_env("ENVIRONMENT")


@pytest.fixture(scope="session")
def service_name():
    return get_env("FULLY_QUALIFIED_SERVICE_NAME")


@pytest.fixture(scope="session")
def service_url(environment):
    if environment == "prod":
        base_url = "https://api.service.nhs.uk"
    else:
        base_url = f"https://{environment}.api.service.nhs.uk"

    service_base_path = get_env("SERVICE_BASE_PATH")

    return f"{base_url}/{service_base_path}"


@pytest.fixture(scope="session")
def status_endpoint_api_key():
    return get_env("STATUS_ENDPOINT_API_KEY")


@pytest.fixture(scope="session")
def asid():
    return get_env("ERS_TEST_ASID")


@pytest.fixture(scope="session")
def token_url():
    oauth_proxy = get_env("OAUTH_PROXY")
    oauth_base_uri = get_env("OAUTH_BASE_URI")
    return f"{oauth_base_uri}/{oauth_proxy}/token"


@pytest.fixture(scope="session")
def app_restricted_ods_code():
    return "RCD"


@pytest.fixture(scope="session")
def app_restricted_user_id():
    return "555032000100"


@pytest.fixture
async def user_restricted_product(make_product):
    # Setup
    product = await make_product(
        ["urn:nhsd:apim:user-nhs-id:aal3:e-referrals-service-api"]
    )
    yield product

    # Teardown
    print(f"Cleanup product: {product.name}")
    await product.destroy_product()


@pytest.fixture
def make_product(environment, service_name):
    async def _make_product(product_scopes):
        # Setup
        product = ApigeeApiProducts()
        await product.create_new_product()

        print(f"CREATED PRODUCT NAME: {product.name}")

        # Update products allowed paths
        proxies = [f"identity-service-mock-{environment}"]

        if service_name is not None:
            proxies.append(service_name)

        await product.update_proxies(proxies)
        await product.update_scopes(scopes=product_scopes)
        return product

    return _make_product


@pytest.fixture
async def user_restricted_app(make_app, user_restricted_product, asid):
    # Setup
    app = await make_app(user_restricted_product, {"asid": asid})

    yield app

    # Teardown
    print(f"Cleanup app: {app.name}")
    await app.destroy_app()


@pytest.fixture
def make_app():
    async def _make_app(product, custom_attributes):
        # Setup
        app = ApigeeApiDeveloperApps()
        await app.create_new_app()

        print(f"CREATED APP NAME: {app.name}")

        # Set ASID
        await app.set_custom_attributes(custom_attributes)

        # Assign the new app to the product
        await app.add_api_product([product.name])

        app.oauth = OauthHelper(app.client_id, app.client_secret, app.callback_url)
        return app

    return _make_app


@pytest.fixture
async def user_restricted_access_code(user_restricted_app, actor):
    token_resp = user_restricted_app.oauth.get_authenticated_with_mock_auth(
        actor.user_id
    )
    print(f"user restricted resp: {token_resp}")
    return token_resp["access_token"]


@pytest.fixture
async def app_restricted_product(make_product):
    # Setup
    product = await make_product(["urn:nhsd:apim:app:level3:e-referrals-service-api"])

    yield product

    # Teardown
    print(f"Cleanup product: {product.name}")
    await product.destroy_product()


@pytest.fixture
async def app_restricted_app(
    make_app,
    app_restricted_product,
    asid,
    app_restricted_ods_code,
    app_restricted_user_id,
):
    # Setup
    app = await make_app(
        app_restricted_product,
        {
            "asid": asid,
            "app-restricted-ods-code": app_restricted_ods_code,
            "app-restricted-user-id": app_restricted_user_id,
            "jwks-resource-url": __JWKS_RESOURCE_URL,
        },
    )

    yield app

    # Teardown
    print(f"Cleanup app: {app.name}")
    await app.destroy_app()


@pytest.fixture
async def app_restricted_access_code(app_restricted_app, token_url):
    jwt = app_restricted_app.oauth.create_jwt(
        **{
            "kid": "test-1",
            "claims": {
                "sub": app_restricted_app.client_id,
                "iss": app_restricted_app.client_id,
                "jti": str(uuid4()),
                "aud": token_url,
                "exp": int(time()) + 60,
            },
        }
    )

    resp = await app_restricted_app.oauth.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    if resp["status_code"] != 200:
        message = "unable to get token"
        raise RuntimeError(
            f"\n{'*' * len(message)}\n"
            f"MESSAGE: {message}\n"
            f"URL: {resp.get('url')}\n"
            f"STATUS CODE: {resp.get('status_code')}\n"
            f"RESPONSE: {resp.get('body')}\n"
            f"HEADERS: {resp.get('headers')}\n"
            f"{'*' * len(message)}\n"
        )
    token_resp = resp["body"]
    print(f"app restricted resp: {token_resp}")
    return token_resp["access_token"]
