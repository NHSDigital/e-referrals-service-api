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
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    testdata = [
        (
            {
                "schedule.actor:HealthcareService": "12000",
                "appointmentType": "ROUTINE",
                "status": "free",
                "_count": "20",
                "page": "1",
            },
            "stu3/retrieveAppointmentSlots/responses/Minimum.json",
            200,
        ),
        (
            {
                "schedule.actor:HealthcareService": "10000",
                "appointmentType": "ROUTINE",
                "status": "free",
                "_count": "20",
                "page": "1",
            },
            "stu3/retrieveAppointmentSlots/responses/NoSlots.json",
            200,
        ),
        (
            {
                "schedule.actor:HealthcareService": "11000",
                "appointmentType": "ROUTINE",
                "status": "free",
                "_count": "5",
                "page": "1",
            },
            "stu3/retrieveAppointmentSlots/responses/Page1PageSize5.json",
            200,
        ),
        (
            {
                "schedule.actor:HealthcareService": "11000",
                "appointmentType": "ROUTINE",
                "status": "free",
                "_count": "5",
                "page": "2",
            },
            "stu3/retrieveAppointmentSlots/responses/Page2PageSize5.json",
            200,
        ),
        (
            {
                "schedule.actor:HealthcareService": "11000",
                "appointmentType": "ROUTINE",
                "status": "free",
                "_count": "5",
                "page": "5",
            },
            "stu3/retrieveAppointmentSlots/responses/ErrorPage5.json",
            400,
        ),
        (
            {
                "schedule.actor:HealthcareService": "13000",
                "appointmentType": "ROUTINE",
                "status": "free",
                "_count": "5",
                "page": "1",
            },
            "stu3/retrieveAppointmentSlots/responses/Page1With2Schedules.json",
            200,
        ),
        (
            {
                "schedule.actor:HealthcareService": "14000",
                "schedule.actor:Practitioner": "921600556514",
                "appointmentType": "ROUTINE",
                "status": "free",
                "_count": "5",
                "page": "1",
            },
            "stu3/retrieveAppointmentSlots/responses/SlotClinicianSearch.json",
            200,
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/Slot"

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
            {
                "schedule.actor:HealthcareService": "12000",
                "appointmentType": "ROUTINE",
                "status": "free",
                "_count": "20",
                "page": "1",
            },
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("params,response, responseCode", testdata)
    def test_success(
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        params,
        response,
        responseCode,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_query(actor, params)

        asserts.assert_status_code(responseCode, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response,
        )
