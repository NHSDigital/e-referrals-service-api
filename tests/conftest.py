import os

import pytest
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps
from api_test_utils.apigee_api_products import ApigeeApiProducts
from api_test_utils.oauth_helper import OauthHelper


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


@pytest.fixture
async def product(environment, service_name):
    # Setup
    product = ApigeeApiProducts()
    await product.create_new_product()

    print(f"CREATED PRODUCT NAME: {product.name}")

    # Update products allowed paths
    proxies = [f"identity-service-mock-{environment}"]

    if service_name is not None:
        proxies.append(service_name)

    await product.update_proxies(proxies)
    await product.update_scopes(
        scopes=["urn:nhsd:apim:user-nhs-id:aal3:e-referrals-service-api"]
    )
    yield product

    # Teardown
    print("Cleanup product")
    await product.destroy_product()


@pytest.fixture
async def app(product, asid):
    # Setup
    app = ApigeeApiDeveloperApps()
    await app.create_new_app()

    print(f"CREATED APP NAME: {app.name}")

    # Set ASID
    await app.set_custom_attributes({"asid": asid})

    # Assign the new app to the product
    await app.add_api_product([product.name])

    app.oauth = OauthHelper(app.client_id, app.client_secret, app.callback_url)

    yield app

    # Teardown
    print("Cleanup app")
    await app.destroy_app()


@pytest.fixture
async def access_code(app, actor):
    token_resp = app.oauth.get_authenticated_with_mock_auth(actor.user_id)

    return token_resp["access_token"]
