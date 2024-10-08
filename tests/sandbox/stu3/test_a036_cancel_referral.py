from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestCancelReferral(SandboxTest):
    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    testdata = [
        (
            "stu3/cancelReferral/requests/IntendPrivateWithoutComment.json",
            "stu3/cancelReferral/responses/CancelledReferralIntendPrivateWithoutComment.json",
        ),
        (
            "stu3/cancelReferral/requests/PatientRequestCancellationOther.json",
            "stu3/cancelReferral/responses/CancelledReferralPatientOther.json",
        ),
        (
            "stu3/cancelReferral/requests/RaisedInError.json",
            "stu3/cancelReferral/responses/CancelledReferralRaisedInError.json",
        ),
        (
            "stu3/cancelReferral/requests/ReferrerCancellation.json",
            "stu3/cancelReferral/responses/CancelledBookedReferralReferrerCancellation.json",
        ),
        (
            "stu3/cancelReferral/requests/NoLongerRequired.json",
            "stu3/cancelReferral/responses/CancelledReferralWithCancelledBookingNoLongerRequired.json",
        ),
        (
            "stu3/cancelReferral/requests/IntendPrivateWithComment.json",
            "stu3/cancelReferral/responses/CancelledReferralResolvedDeferralIntendPrivateWithComment.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/ReferralRequest/000000070000/$ers.cancelReferral"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestCancelReferral.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestCancelReferral.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor,
            "stu3/cancelReferral/requests/ReferrerCancellation.json",
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
