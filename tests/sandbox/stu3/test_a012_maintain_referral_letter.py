from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestMaintainReferralLetter(SandboxTest):
    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    testdata = [
        (
            "000000070000",
            "stu3/maintainReferralLetter/requests/SingleDocumentReference.json",
            "stu3/maintainReferralLetter/responses/ReferralRequestWithSingleDocumentReference.json",
        ),
        (
            "000000070001",
            "stu3/maintainReferralLetter/requests/MultipleDocumentReferences.json",
            "stu3/maintainReferralLetter/responses/ReferralRequestWithMultipleDocumentReferences.json",
        ),
        (
            "000000070001",
            "stu3/maintainReferralLetter/requests/UpdateClinicalInfo.json",
            "stu3/maintainReferralLetter/responses/ReferralRequestWithUpdatedDocumentReferences.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/ReferralRequest/{ubrn}/$ers.maintainReferralLetter"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestMaintainReferralLetter.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestMaintainReferralLetter.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_pathParam_and_request: Callable[
            [Actor, str, Dict[str, str], Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_pathParam_and_request(
            actor,
            "stu3/maintainReferralLetter/requests/SingleDocumentReference.json",
            {"ubrn": "000000070000"},
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("ubrn,requestJson,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_pathParam_and_request: Callable[
            [Actor, str, Dict[str, str], Dict[str, str]], Response
        ],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        ubrn,
        requestJson,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_pathParam_and_request(
            actor, requestJson, {"ubrn": ubrn}
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response,
            additional={
                "etag": 'W/"5"',
            },
        )
