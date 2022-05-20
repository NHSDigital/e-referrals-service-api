from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestAcceptReferral(SandboxTest):
    authorised_actor_data = [Actor.SPC, Actor.SPCA]

    allowed_business_function_data = [
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestAcceptReferral.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestAcceptReferral.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self, send_rest_request: Callable[[HttpMethod, str, Actor], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: send_rest_request(
            HttpMethod.POST,
            "FHIR/STU3/ReferralRequest/000000070000/$ers.acceptReferral",
            actor,
            headers=headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    def test_success(
        self,
        call_endpoint: Callable[[Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
    ):

        actual_response = call_endpoint(actor)

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(
            load_json("acceptReferral/responses/ExampleResponse.json"), actual_response,
        )

        asserts.assert_headers(
            actual_response, additional={"etag": 'W/"9"',},
        )
