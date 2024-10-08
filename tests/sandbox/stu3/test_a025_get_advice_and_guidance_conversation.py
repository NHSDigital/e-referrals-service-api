from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestGetAdviceAndGuidanceConversation(SandboxTest):
    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    testdata = [
        (
            "CommunicationRequest/000000070000/_history/1",
            "stu3/retrieveAdviceAndGuidanceConversation/SingleMessageFromReferrer.json",
            'W/"1"',
        ),
        (
            "CommunicationRequest/000000070000/_history/2",
            "stu3/retrieveAdviceAndGuidanceConversation/OneMessageEachWay.json",
            'W/"2"',
        ),
        (
            "CommunicationRequest/000000070001/_history/6",
            "stu3/retrieveAdviceAndGuidanceConversation/AttachmentPresentInEachDirection.json",
            'W/"6"',
        ),
        (
            "CommunicationRequest/000000070002/_history/1",
            "stu3/retrieveAdviceAndGuidanceConversation/MultiWayConversation.json",
            'W/"6"',
        ),
        (
            "CommunicationRequest/000000070003/_history/7",
            "stu3/retrieveAdviceAndGuidanceConversation/AttachmentUploadedFromRCS.json",
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
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
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
            actual_response,
            additional={
                "etag": etag,
            },
        )
