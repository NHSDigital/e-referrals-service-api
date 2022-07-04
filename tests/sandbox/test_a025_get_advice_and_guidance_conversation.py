from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestGetAdviceAndGuidanceConversation(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA, Actor.RC_DEV, Actor.SPC, Actor.SPCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    testdata = [
        (
            "CommunicationRequest/000000070000/_history/1",
            "retrieveAdviceAndGuidanceConversation/SingleMessageFromReferrer.json",
            'W/"1"',
        ),
        (
            "CommunicationRequest/000000070000/_history/2",
            "retrieveAdviceAndGuidanceConversation/OneMessageEachWay.json",
            'W/"2"',
        ),
        (
            "CommunicationRequest/000000070001/_history/6",
            "retrieveAdviceAndGuidanceConversation/AttachmentPresentInEachDirection.json",
            'W/"6"',
        ),
        (
            "CommunicationRequest/000000070002/_history/1",
            "retrieveAdviceAndGuidanceConversation/MultiWayConversation.json",
            'W/"6"',
        ),
        (
            "CommunicationRequest/000000070003/_history/7",
            "retrieveAdviceAndGuidanceConversation/AttachmentUploadedFromRCS.json",
            'W/"7"',
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/Communication"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.GET

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestGetAdviceAndGuidanceConversation.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestGetAdviceAndGuidanceConversation.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self, call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_query(
            actor,
            {"based-on": "CommunicationRequest/000000070000/_history/1"},
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("basedOn,response, etag", testdata)
    def test_success(
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        basedOn,
        response,
        etag,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_query(actor, {"based-on": basedOn})

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response, additional={"etag": etag,},
        )
