from typing import Callable, Dict, Iterable

import pytest
import asserts

from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod
from requests import Response


@pytest.mark.sandbox
class TestCreateReferralSendForTriage(SandboxTest):
    authorised_actor_data = [
        Actor.RC,
        Actor.RC_DEV,
        Actor.RC_INSUFFICIENT_IAL,
        Actor.RCA,
    ]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    testdata = [
        (
            Actor.RC,
            "stu3/createReferralAndSendForTriage/requests/Parameters.json",
            "stu3/createReferralAndSendForTriage/responses/ReferralRequest.json",
        ),
        (
            Actor.RCA,
            "stu3/createReferralAndSendForTriage/requests/ParametersWithNamedClinician.json",
            "stu3/createReferralAndSendForTriage/responses/ReferralRequestWithNamedClinician.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/ReferralRequest/$ers.createReferralAndSendForTriage"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestCreateReferralSendForTriage.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestCreateReferralSendForTriage.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor,
            self._request_path(actor),
            headers,
        )

    @pytest.mark.parametrize("actor, requestJson, response", testdata)
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

        asserts.assert_status_code(201, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)
        asserts.assert_json_response_headers(
            actual_response,
            additional={
                "etag": 'W/"1"',
            },
        )

    def _request_path(self, actor: Actor) -> str:
        path = (
            "stu3/createReferralAndSendForTriage/requests/ParametersWithNamedClinician.json"
            if actor == Actor.RCA
            else "stu3/createReferralAndSendForTriage/requests/Parameters.json"
        )
        return path
