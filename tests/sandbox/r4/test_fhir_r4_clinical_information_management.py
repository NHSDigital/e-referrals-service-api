from typing import Callable, Dict, Iterable

import pytest
import requests
from requests import Response

from tests import asserts
from tests.data import Actor, RenamedHeader
from tests.sandbox.SandboxTest import SandboxTest
from tests.sandbox.utils import HttpMethod

_HTTP_ERROR_CODES = "https://fhir.nhs.uk/CodeSystem/http-error-codes"
_ERS_ERROR_CODES = "https://fhir.nhs.uk/CodeSystem/ers-error-codes"


def _assert_operation_outcome(
    response: Response, system: str, code: str, diagnostics: str
):
    assert response.headers["content-type"].startswith("application/fhir+json")
    body = response.json()
    assert body["resourceType"] == "OperationOutcome"
    issue = body["issue"][0]
    assert issue["severity"] == "error"
    assert issue["details"]["coding"][0] == {"system": system, "code": code}
    assert issue["diagnostics"] == diagnostics


@pytest.mark.sandbox
class TestClinicalInformationManagement(SandboxTest):
    allowed_business_function_data = [
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    examples = [
        (
            "r4/clinicalInformationManagement/requests/singleAttachment.json",
            "r4/clinicalInformationManagement/responses/singleAttachment.json",
            1,
        ),
        (
            "r4/clinicalInformationManagement/requests/" "multipleAttachments.json",
            "r4/clinicalInformationManagement/responses/" "multipleAttachments.json",
            2,
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/R4"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestClinicalInformationManagement.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestClinicalInformationManagement.allowed_business_function_data

    @pytest.fixture
    def default_headers(self) -> Dict[str, str]:
        return {"content-type": "application/fhir+json"}

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor,
            "r4/clinicalInformationManagement/requests/singleAttachment.json",
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("request_fixture,response_fixture,entry_count", examples)
    def test_success(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        request_fixture: str,
        response_fixture: str,
        entry_count: int,
    ):
        actual_response = call_endpoint_url_with_request(
            actor,
            request_fixture,
            {"content-type": "application/fhir+json"},
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(load_json(response_fixture), actual_response)
        assert len(actual_response.json()["entry"]) == entry_count
        assert actual_response.headers["content-type"].startswith(
            "application/fhir+json"
        )

    @pytest.mark.parametrize(
        "mutate,expected_status,expected_system,expected_code," "expected_diagnostics",
        [
            (
                lambda body: body.update({"type": "collection"}),
                400,
                _HTTP_ERROR_CODES,
                "REC_BAD_REQUEST",
                "Bundle.type must be transaction",
            ),
            (
                lambda body: body["entry"][0].update({"fullUrl": "not a uri"}),
                400,
                _HTTP_ERROR_CODES,
                "REC_BAD_REQUEST",
                "Bundle.entry.fullUrl must be an absolute URI",
            ),
            (
                lambda body: body["entry"][0]["resource"].update(
                    {"date": "2026-10-16T09:30"}
                ),
                400,
                _HTTP_ERROR_CODES,
                "REC_BAD_REQUEST",
                "DocumentReference.date must be a valid FHIR R4 dateTime",
            ),
            (
                lambda body: body.update({"entry": []}),
                422,
                _HTTP_ERROR_CODES,
                "REC_BAD_REQUEST",
                "Bundle.entry must contain at least one DocumentReference",
            ),
            (
                lambda body: body["entry"][1]["resource"]["subject"][
                    "identifier"
                ].update({"value": "000000070001"}),
                422,
                _HTTP_ERROR_CODES,
                "REC_BAD_REQUEST",
                "Multiple different UBRNs in one transaction",
            ),
            (
                lambda body: body["entry"][1]["resource"]["content"][0][
                    "attachment"
                ].update({"url": "Binary/d497bbe3-f88b-45f1-b3d4-9c563e4c0f5f"}),
                422,
                _ERS_ERROR_CODES,
                "CONFLICTING_VALUES",
                "Binary/d497bbe3-f88b-45f1-b3d4-9c563e4c0f5f cannot be "
                "linked to the referral more than once",
            ),
        ],
    )
    def test_invalid_request(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
        http_method: HttpMethod,
        default_headers: Dict[str, str],
        mutate: Callable[[Dict], None],
        expected_status: int,
        expected_system: str,
        expected_code: str,
        expected_diagnostics: str,
    ):
        request_body = load_json(
            "r4/clinicalInformationManagement/requests/" "multipleAttachments.json"
        )
        mutate(request_body)

        actual_response = send_rest_request(
            http_method,
            endpoint_url,
            Actor.SPC,
            headers=default_headers,
            json=request_body,
        )

        asserts.assert_status_code(expected_status, actual_response.status_code)
        _assert_operation_outcome(
            actual_response,
            expected_system,
            expected_code,
            expected_diagnostics,
        )

    def test_malformed_json_returns_bad_request(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        endpoint_url: str,
        http_method: HttpMethod,
        default_headers: Dict[str, str],
    ):
        actual_response = send_rest_request(
            http_method,
            endpoint_url,
            Actor.SPC,
            headers=default_headers,
            data="{not json",
        )

        asserts.assert_status_code(400, actual_response.status_code)
        _assert_operation_outcome(
            actual_response,
            _HTTP_ERROR_CODES,
            "REC_BAD_REQUEST",
            "Request body must be valid FHIR R4 JSON",
        )

    def test_spc_with_obo_user_is_forbidden(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
        http_method: HttpMethod,
        default_headers: Dict[str, str],
    ):
        default_headers[RenamedHeader.OBO_USER_ID.original] = "021600556514"

        actual_response = send_rest_request(
            http_method,
            endpoint_url,
            Actor.SPC,
            headers=default_headers,
            json=load_json(
                "r4/clinicalInformationManagement/requests/" "singleAttachment.json"
            ),
        )

        asserts.assert_status_code(403, actual_response.status_code)

    def test_spca_without_obo_user_is_forbidden(
        self,
        sandbox_url: str,
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
        default_headers: Dict[str, str],
    ):
        # send_rest_request always adds the SPCA OBO header, so call directly.
        default_headers[RenamedHeader.BUSINESS_FUNCTION.original] = (
            Actor.SPCA.business_function
        )

        actual_response = requests.post(
            f"{sandbox_url}/{endpoint_url}",
            headers=default_headers,
            json=load_json(
                "r4/clinicalInformationManagement/requests/" "singleAttachment.json"
            ),
        )

        asserts.assert_status_code(403, actual_response.status_code)

    @pytest.mark.parametrize(
        "comment_length,expected_status", [(2000, 200), (2001, 422)]
    )
    def test_comment_max_length(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
        http_method: HttpMethod,
        default_headers: Dict[str, str],
        comment_length: int,
        expected_status: int,
    ):
        request_body = load_json(
            "r4/clinicalInformationManagement/requests/singleAttachment.json"
        )
        request_body["extension"][0]["valueString"] = "a" * comment_length

        actual_response = send_rest_request(
            http_method,
            endpoint_url,
            Actor.SPC,
            headers=default_headers,
            json=request_body,
        )

        asserts.assert_status_code(expected_status, actual_response.status_code)
