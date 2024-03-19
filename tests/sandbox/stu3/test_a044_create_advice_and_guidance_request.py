from typing import Callable, Dict, Iterable

import pytest
import asserts

from requests import Response

from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod

authorised_actor_data = [Actor.RC, Actor.RC_DEV, Actor.RCA]


@pytest.mark.sandbox
class TestCreateAdviceAndGuidance(SandboxTest):

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    request_path = "stu3/createAdviceAndGuidance/requests/ExampleAdviceAndGuidance.json"

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/CommunicationRequest/$ers.createAdviceAndGuidance"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return self.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor, self.request_path, headers
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    def test_success(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
    ):
        expected_response = load_json(
            "stu3/createAdviceAndGuidance/responses/ExampleAdviceAndGuidance.json"
        )
        actual_response = call_endpoint_url_with_request(actor, self.request_path)

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)
        asserts.assert_json_response_headers(actual_response)
