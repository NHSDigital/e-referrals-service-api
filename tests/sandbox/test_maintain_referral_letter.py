from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestMaintainReferralLetter(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]
    testdata = [
        (
            "000000070000",
            "maintainReferralLetter/requests/SingleDocumentReference.json",
            "maintainReferralLetter/responses/ReferralRequestWithSingleDocumentReference.json",
        ),
        (
            "000000070001",
            "maintainReferralLetter/requests/MultipleDocumentReferences.json",
            "maintainReferralLetter/responses/ReferralRequestWithMultipleDocumentReferences.json",
        ),
        (
            "000000070001",
            "maintainReferralLetter/requests/UpdateClinicalInfo.json",
            "maintainReferralLetter/responses/ReferralRequestWithUpdatedDocumentReferences.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/ReferralRequest/{param}/$ers.maintainReferralLetter"

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestMaintainReferralLetter.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestMaintainReferralLetter.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_value_and_request: Callable[[Actor, str, str], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_value_and_request(
            actor,
            "maintainReferralLetter/requests/SingleDocumentReference.json",
            "000000070000",
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("ubrn,requestJson,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_value_and_request: Callable[[Actor, str, str], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        ubrn,
        requestJson,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_value_and_request(
            actor, requestJson, ubrn
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response, additional={"etag": 'W/"5"',},
        )
