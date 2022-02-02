import os

import pytest
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps
from api_test_utils.apigee_api_products import ApigeeApiProducts
from api_test_utils.oauth_helper import OauthHelper
from time import time


DEFAULT_ASID = '1234567890'
DEFAULT_USERID = '9999999999'


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
    base_url = "https://api.service.nhs.uk" if environment == "prod" else f"https://{environment}.api.service.nhs.uk"
    service_base_path = get_env('SERVICE_BASE_PATH')

    return f"{base_url}/{service_base_path}"


@pytest.fixture(scope="session")
def status_endpoint_api_key():
    return get_env("STATUS_ENDPOINT_API_KEY")


@pytest.fixture(scope="session")
def id_token_key():
    id_token_key_path = get_env("ID_TOKEN_TESTING_PRIVATE_KEY_ABSOLUTE_PATH")

    with open(id_token_key_path, "r") as f:
        return f.read()


@pytest.fixture(scope="session")
def asid():
    return DEFAULT_ASID


@pytest.fixture(scope="session")
def user_id():
    return DEFAULT_USERID


@pytest.fixture
async def product(environment, service_name):
    # Setup
    product = ApigeeApiProducts()
    await product.create_new_product()

    print('CREATED PRODUCT NAME: ' + product.name)

    # Update products allowed paths
    await product.update_proxies([service_name, 'identity-service-' + environment])

    await product.update_scopes(
        scopes=["urn:nhsd:apim:user-nhs-id:aal3:e-referrals-service-api"]
    )
    yield product

    # Teardown
    print('Cleanup product')
    await product.destroy_product()


@pytest.fixture
async def app(environment, product, asid):
    # Setup
    app = ApigeeApiDeveloperApps()
    await app.create_new_app()

    print('CREATED APP NAME: ' + app.name)

    # Set default JWT Testing resource url and ASID
    await app.set_custom_attributes({
            'asid': asid,
            'jwks-resource-url': 'https://raw.githubusercontent.com/NHSDigital/'
                                 f'identity-service-jwks/main/jwks/{environment}/'
                                 '9baed6f4-1361-4a8e-8531-1f8426e3aba8.json'
    })

    # Assign the new app to the product
    await app.add_api_product([product.name])

    yield app

    # Teardown
    print('Cleanup app')
    await app.destroy_app()


@pytest.fixture
async def access_code(app, id_token_key, user_id):
    oauth = OauthHelper(app.client_id, app.client_secret, app.callback_url)

    claims = {
            'at_hash': 'tf_-lqpq36lwO7WmSBIJ6Q',
            'sub': user_id,
            'auditTrackingId': '91f694e6-3749-42fd-90b0-c3134b0d98f6-1546391',
            'amr': ['N3_SMARTCARD'],
            'iss': 'https://am.nhsint.auth-ptl.cis2.spineservices.nhs.uk:443/'
                   'openam/oauth2/realms/root/realms/NHSIdentity/realms/Healthcare',
            'tokenName': 'id_token',
            'aud': '969567331415.apps.national',
            'c_hash': 'bc7zzGkClC3MEiFQ3YhPKg',
            'acr': 'AAL3_ANY',
            'org.forgerock.openidconnect.ops': '-I45NjmMDdMa-aNF2sr9hC7qEGQ',
            's_hash': 'LPJNul-wow4m6Dsqxbning',
            'azp': '969567331415.apps.national',
            'auth_time': int(time()),
            'realm': '/NHSIdentity/Healthcare',
            'exp': int(time()) + 6000,
            'tokenType': 'JWTToken',
            'iat': int(time()) - 100
    }

    print('Claims:')
    print(claims)

    client_assertion_jwt = oauth.create_jwt(kid='test-1')
    id_token_jwt = oauth.create_id_token_jwt(algorithm="RS512", kid="identity-service-tests-1", claims=claims, signing_key=id_token_key)

    resp = await oauth.get_token_response(
        grant_type="token_exchange",
        _jwt=client_assertion_jwt,
        id_token_jwt=id_token_jwt
    )
    print('JWT Token response:')
    print(resp)

    return resp['body']['access_token']
