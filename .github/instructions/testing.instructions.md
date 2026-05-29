---
applyTo: "tests/**"
description: "Test structure, Actor model, activity codes, SandboxTest base class, integration test setup, and how to add new tests"
---

# Test Structure

Tests use **pytest** and live under `tests/`. Three suites: `sandbox/`, `integration/`, `smoke/`.

## Test markers

Defined in `pyproject.toml`:
- `sandbox` — sandbox tests (applied via `SandboxTest` base class)
- `integration_test` — integration tests against deployed environments
- `smoke_test` — health/status checks

## Actor model (`tests/data.py`)

The `Actor` enum models different e-RS user personas. Each actor has:

| Property | Description |
|---|---|
| `user_id` | Simulated NHS user ID |
| `org_code` | ODS organisation code |
| `business_function` | e-RS business function (role) |
| `id_assurance_level` | IAL (identity assurance level, typically `"3"`) |
| `authentication_assurance_level` | AAL enum (`AAL3`, `AAL2`, `AAL1`) |
| `obo_user_id` | Optional on-behalf-of user ID (only for `SPCA`) |

### Standard actors

| Actor | Business function | ODS | Notes |
|---|---|---|---|
| `RC` | `REFERRING_CLINICIAN` | `D82106` | Primary care referrer |
| `RCA` | `REFERRING_CLINICIAN_ADMIN` | `D82106` | Referrer admin |
| `RA` | `REFERRING_ADMIN` | `D82106` | Referring admin |
| `SPC` | `SERVICE_PROVIDER_CLINICIAN` | `RCD` | Secondary care clinician |
| `SPA` | `SERVICE_PROVIDER_ADMIN` | `RCD` | Provider admin |
| `SPCA` | `SERVICE_PROVIDER_CLINICIAN_ADMIN` | `RCD` | Provider admin acting on behalf of another user |
| `RC_DEV` | `REFERRING_CLINICIAN` | `R69` | Dev/integration test user |
| `RC_INSUFFICIENT_IAL` | `REFERRING_CLINICIAN` | `D82106` | IAL=2, used for auth failure tests |
| `AAL2_USER` | `REFERRING_CLINICIAN` | `RCD` | AAL2 auth level |
| `AAL1_USER` | `REFERRING_CLINICIAN` | `RCD` | AAL1 auth level (should be rejected) |

Helper method: `actor.is_referrer()` returns `True` for RC, RCA, RA business functions.

### Header mapping (`RenamedHeader`)

The `RenamedHeader` enum maps external header names to internal names — used by test fixtures to set correct headers when calling the sandbox.

## Activity code naming convention

Test files are named by **e-RS activity code**: `test_a030_retrieve_eRS_business_functions.py`, `test_a033_retrieve_healthcare_service.py`, etc.

These codes (`a030`, `a033`, `a035`, ...) correspond to specific API operations defined in the e-RS service specification. When adding a new test file, use the activity code assigned to the endpoint in the e-RS documentation.

## Sandbox tests (`tests/sandbox/`)

### Running
```bash
make sandbox-tests
# or directly:
ENVIRONMENT=local SERVICE_BASE_PATH=localhost poetry run pytest -v tests/sandbox
```
Requires the sandbox running locally on port 9100.

### `SandboxTest` base class

All sandbox test classes extend `SandboxTest` (in `tests/sandbox/SandboxTest.py`), which provides:

**Required fixtures (abstract — must be implemented):**
- `endpoint_url` — the API path to test
- `http_method` — `HttpMethod` enum (GET, POST, PUT, etc.)
- `authorised_actors` — list of `Actor` values allowed to call this endpoint
- `default_headers` — headers to include in every request
- `call_endpoint` — function that sends the request and returns the response
- `allowed_business_functions` — list of business function strings permitted

**Derived fixtures:**
- `unauthorised_actors` — automatically computed as all actors NOT in `authorised_actors`

**Built-in tests (inherited automatically):**
- `test_unauthorised_business_functions` — verifies 403 for all unauthorised actors, checks the error message matches the expected `SANDBOX_ERROR:` format
- `test_with_correlation_id` — verifies `X-Correlation-ID` is echoed back in responses

### Key conftest fixtures (`tests/sandbox/conftest.py`)

- `sandbox_url` — resolves to `http://127.0.0.1:9100` locally or the deployed service URL
- `load_json(path)` — loads a JSON fixture from `sandbox/src/mocks/`
- `load_file(path)` — loads a binary fixture (e.g. PDF)
- `send_rest_request(method, url, actor, headers)` — sends an HTTP request with actor-appropriate headers

### Assertion utilities (`tests/asserts.py`)

- `assert_status_code(expected, actual)` — status code check with `pytest_check`
- `assert_response(expected_dict, actual_response)` — full JSON body comparison
- Generic header sets (`_generic_headers`, `_generic_file_headers`) define expected response headers

## Integration tests (`tests/integration/`)

### Running
Require a deployed Apigee environment. Env vars needed:
- `ENVIRONMENT`, `FULLY_QUALIFIED_SERVICE_NAME`, `SERVICE_BASE_PATH`
- `OAUTH_PROXY`, `OAUTH_BASE_URI`
- ASID-related variables

### Files
- `test_user_restricted.py` — user-restricted OAuth flow, validates ODS/business function behaviour
- `test_app_restricted.py` — app-restricted (client credentials) flow
- `test_headers.py` — header validation across endpoints

### Key dependency
Uses `pytest-nhsd-apim` for OAuth authenticators (`AuthorizationCodeAuthenticator`, `ClientCredentialsAuthenticator`) and Apigee API management (`ApigeeClient`, `ApiProductsAPI`).

## Smoke tests (`tests/smoke/`)

`test_status_endpoints.py` — basic `_ping` and `_status` health checks.

## Adding a new test

1. Identify the e-RS activity code for the endpoint
2. Create `tests/sandbox/{stu3,r4}/test_a{code}_{endpoint_name}.py`
3. Extend `SandboxTest`, implement all abstract fixtures
4. Define `authorised_actors` matching the sandbox route's `allowedBusinessFunctions`
5. The base class auto-tests unauthorised actors and correlation ID handling
6. Add endpoint-specific tests (response body, headers, status codes, edge cases)
