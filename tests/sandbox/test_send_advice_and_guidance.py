from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestSendAdviceAndGuidance(SandboxTest):
    authorised_actor_data = [Actor.SPC, Actor.SPCA]

    allowed_business_function_data = [
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    testdata = [
        (
            "sendAdviceAndGuidanceResponse/requests/RequireFurtherInformation.json",
            "sendAdviceAndGuidanceResponse/responses/RequireFurtherInformation.json",
        ),
        (
            "sendAdviceAndGuidanceResponse/requests/ReturnToReferrerWithAdvice.json",
            "sendAdviceAndGuidanceResponse/responses/ReturnToReferrerWithAdvice.json",
        ),
        (
            "sendAdviceAndGuidanceResponse/requests/AttachmentIncluded.json",
            "sendAdviceAndGuidanceResponse/responses/AttachmentIncluded.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/CommunicationRequest/000000070000/$ers.sendCommunicationToRequester"

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestSendAdviceAndGuidance.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestSendAdviceAndGuidance.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor,
            "sendAdviceAndGuidanceResponse/requests/RequireFurtherInformation.json",
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("requestJson,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        requestJson,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_request(actor, requestJson)

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(actual_response)
