from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestBookOrDeferAppointment(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]
    testdata = [
        (
            "bookOrDeferAppointment/requests/MinimalBooking.json",
            "bookOrDeferAppointment/responses/MinimalBooking.json",
        ),
        (
            "bookOrDeferAppointment/requests/MinimalDeferral.json",
            "bookOrDeferAppointment/responses/MinimalDeferral.json",
        ),
        (
            "bookOrDeferAppointment/requests/BookingWithNamedClinician.json",
            "bookOrDeferAppointment/responses/BookingWithNamedClinician.json",
        ),
        (
            "bookOrDeferAppointment/requests/DeferralWithSlotReference.json",
            "bookOrDeferAppointment/responses/DeferralWithSlotReference.json",
        ),
        (
            "bookOrDeferAppointment/requests/DeferralBookingAttemptProblem.json",
            "bookOrDeferAppointment/responses/DeferralBookingAttemptProblem.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/Appointment"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestBookOrDeferAppointment.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestBookOrDeferAppointment.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor, "bookOrDeferAppointment/requests/MinimalBooking.json", headers,
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

        asserts.assert_status_code(201, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response, additional={"etag": 'W/"1"',},
        )
