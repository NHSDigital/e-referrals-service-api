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
    @pytest.fixture
    def unauthorised_actors(self) -> Iterable[Actor]:
        return self.unauthorised_actors_list()

    def unauthorised_actors_list(self) -> List[Actor]:
        return [Actor.AA]

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        authorised = []
        for actor in Actor:
            if actor not in self.unauthorised_actors_list():
                authorised.append(actor)
        return authorised

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return [
            "SERVICE_PROVIDER_CLINICIAN",
            "SERVICE_PROVIDER_ADMIN",
            "SERVICE_PROVIDER_CLINICIAN_ADMIN",
            "REFERRING_CLINICIAN",
            "REFERRING_CLINICIAN_ADMIN",
            "REFERRING_ADMIN",
        ]

    @pytest.fixture
    def call_endpoint(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: send_rest_request(
            HttpMethod.POST,
            "FHIR/STU3/ReferralRequest/$ers.fetchworklist",
            actor,
            json=load_json("retrieveWorklist/requests/MinimalReferralsForReview.json"),
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint_with_request(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor, str], Response]:
        return lambda actor, requestJson, headers={}: send_rest_request(
            HttpMethod.POST,
            "FHIR/STU3/ReferralRequest/$ers.fetchworklist",
            actor,
            json=load_json(requestJson),
            headers=headers,
        )

    testdata = [
        (
            "retrieveWorklist/requests/MinimalReferralsForReview.json",
            "retrieveWorklist/responses/ReferralsForReview.json",
        ),
        (
            "retrieveWorklist/requests/MinimalAppointmentSlotIssues.json",
            "retrieveWorklist/responses/AppointmentSlotIssues.json",
        ),
        (
            "retrieveWorklist/requests/FilteringBySpecialty.json",
            "retrieveWorklist/responses/FilteredBySpecialty.json",
        ),
        (
            "retrieveWorklist/requests/FilteringByClinician.json",
            "retrieveWorklist/responses/FilteredByClinician.json",
        ),
        (
            "retrieveWorklist/requests/MinimalRejectedTriageResponse.json",
            "retrieveWorklist/responses/RejectedTriageResponse.json",
        ),
        (
            "retrieveWorklist/requests/MinimalAssessmentReturnedCancelledDna.json",
            "retrieveWorklist/responses/AssessmentReturnedCancelledDna.json",
        ),
        (
            "retrieveWorklist/requests/MinimalAwaitingBooking.json",
            "retrieveWorklist/responses/AwaitingBooking.json",
        ),
        (
            "retrieveWorklist/requests/MinimalLettersOutstanding.json",
            "retrieveWorklist/responses/LettersOutstanding.json",
        ),
    ]

    @pytest.mark.parametrize(
        "actor", [Actor.RC, Actor.RCA, Actor.RA, Actor.SPC, Actor.SPCA, Actor.SPA]
    )
    @pytest.mark.parametrize("requestJson,response", testdata)
    def test_success(
        self,
        call_endpoint_with_request: Callable[[Actor, str], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        requestJson,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_with_request(actor, requestJson)

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_headers(actual_response)
