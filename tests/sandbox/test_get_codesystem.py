from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestGetCodesystem(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA, Actor.SPC, Actor.SPCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    testdata = [
        ("SPECIALTY", "getCodeSystem/responses/SpecialtyCodeSystem.json",),
        ("CLINIC-TYPE", "getCodeSystem/responses/ClinicTypeCodeSystem.json",),
        (
            "APPOINTMENT-CANCELLATION-REASON",
            "getCodeSystem/responses/AppointmentCancellationReasonCodeSystem.json",
        ),
        (
            "REFERRAL-CANCELLATION-REASON",
            "getCodeSystem/responses/ReferralCancellationReasonCodeSystem.json",
        ),
        (
            "APPOINTMENT-NON-ATTENDANCE-REASON",
            "getCodeSystem/responses/AppointmentNonAttendanceReasonCodeSystem.json",
        ),
        ("PRIORITY", "getCodeSystem/responses/PriorityCodeSystem.json"),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/CodeSystem/{param}"

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestGetCodesystem.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestGetCodesystem.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self, call_endpoint_url_with_value: Callable[[Actor, str], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_value(
            actor, "SPECIALTY", headers
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("specialty,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_value: Callable[[Actor, str], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        specialty,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_value(actor, specialty)

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_headers(actual_response)
