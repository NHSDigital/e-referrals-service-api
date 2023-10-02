from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestGetReferralWorklist(SandboxTest):
    authorised_actor_data = [
        Actor.RC,
        Actor.RC_DEV,
        Actor.RCA,
        Actor.RA,
        Actor.SPC,
        Actor.SPCA,
        Actor.SPA,
    ]

    allowed_business_function_data = [
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "REFERRING_ADMIN",
    ]

    testdata = [
        (
            "stu3/retrieveWorklist/requests/MinimalReferralsForReview.json",
            "stu3/retrieveWorklist/responses/ReferralsForReview.json",
        ),
        (
            "stu3/retrieveWorklist/requests/MinimalAppointmentSlotIssues.json",
            "stu3/retrieveWorklist/responses/AppointmentSlotIssues.json",
        ),
        (
            "stu3/retrieveWorklist/requests/FilteringBySpecialty.json",
            "stu3/retrieveWorklist/responses/FilteredBySpecialty.json",
        ),
        (
            "stu3/retrieveWorklist/requests/FilteringByClinician.json",
            "stu3/retrieveWorklist/responses/FilteredByClinician.json",
        ),
        (
            "stu3/retrieveWorklist/requests/MinimalRejectedTriageResponse.json",
            "stu3/retrieveWorklist/responses/RejectedTriageResponse.json",
        ),
        (
            "stu3/retrieveWorklist/requests/MinimalAssessmentReturnedCancelledDna.json",
            "stu3/retrieveWorklist/responses/AssessmentReturnedCancelledDna.json",
        ),
        (
            "stu3/retrieveWorklist/requests/MinimalAwaitingBooking.json",
            "stu3/retrieveWorklist/responses/AwaitingBooking.json",
        ),
        (
            "stu3/retrieveWorklist/requests/MinimalLettersOutstanding.json",
            "stu3/retrieveWorklist/responses/LettersOutstanding.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/ReferralRequest/$ers.fetchworklist"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestGetReferralWorklist.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestGetReferralWorklist.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor,
            "stu3/retrieveWorklist/requests/MinimalReferralsForReview.json",
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
