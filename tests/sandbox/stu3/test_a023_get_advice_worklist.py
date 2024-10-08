from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestGetAdviceWorklist(SandboxTest):
    authorised_actor_data = [Actor.SPC, Actor.SPA, Actor.SPCA]

    allowed_business_function_data = [
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    testdata = [
        (
            "stu3/retrieveAdviceAndGuidanceWorklist/requests/MinimalAdviceAndGuidanceRequests.json",
            "stu3/retrieveAdviceAndGuidanceWorklist/responses/AdviceAndGuidanceRequests.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/CommunicationRequest/$ers.fetchworklist"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestGetAdviceWorklist.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestGetAdviceWorklist.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor,
            "stu3/retrieveAdviceAndGuidanceWorklist/requests/MinimalAdviceAndGuidanceRequests.json",
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
