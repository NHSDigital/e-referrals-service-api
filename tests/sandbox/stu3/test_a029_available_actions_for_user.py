from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestAvailableActionsForUser(SandboxTest):
    allowed_business_function_data = [
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    testdata = [
        (
            {
                "focus": "ReferralRequest/000000070000/_history/6",
                "intent": "proposal",
                "status": "ready",
            },
            "stu3/availableActionsForUserList/Empty.json",
        ),
        (
            {
                "focus": "ReferralRequest/000000070001/_history/6",
                "intent": "proposal",
                "status": "ready",
            },
            "stu3/availableActionsForUserList/WithRecordReviewOutcome.json",
        ),
        (
            {
                "focus": "ReferralRequest/000000070002/_history/6",
                "intent": "proposal",
                "status": "ready",
            },
            "stu3/availableActionsForUserList/WithCreateAppointment.json",
        ),
        (
            {
                "focus": "ReferralRequest/000000070003/_history/6",
                "intent": "proposal",
                "status": "ready",
            },
            "stu3/availableActionsForUserList/WithChangeShortlist.json",
        ),
        (
            {
                "focus": "ReferralRequest/000000070004/_history/6",
                "intent": "proposal",
                "status": "ready",
            },
            "stu3/availableActionsForUserList/WithChangeShortlistAndSendForTriage.json",
        ),
        (
            {
                "focus": "ReferralRequest/000000070005/_history/6",
                "intent": "proposal",
                "status": "ready",
            },
            "stu3/availableActionsForUserList/WithCancelReferral.json",
        ),
        (
            {
                "focus": "ReferralRequest/000000070006/_history/6",
                "intent": "proposal",
                "status": "ready",
            },
            "stu3/availableActionsForUserList/WithCancelDBAppointment.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/Task"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.GET

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestAvailableActionsForUser.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestAvailableActionsForUser.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_query(
            actor,
            {
                "focus": "ReferralRequest/000000070000/_history/6",
                "intent": "proposal",
                "status": "ready",
            },
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("params,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        params,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_query(actor, params)

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response,
        )
