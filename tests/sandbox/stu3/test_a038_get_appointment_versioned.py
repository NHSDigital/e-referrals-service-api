from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestGetAppointment(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA, Actor.RC_DEV, Actor.SPC, Actor.SPCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    testdata = [
        ("70000", "stu3/retrieveAppointment/responses/BookedDBS.json",),
        ("70001", "stu3/retrieveAppointment/responses/BookedIBS.json",),
        ("70002", "stu3/retrieveAppointment/responses/AppointmentDeferral.json",),
        ("70003", "stu3/retrieveAppointment/responses/TriageDeferral.json",),
        ("70004", "stu3/retrieveAppointment/responses/TriageResponse.json",),
        ("70005", "stu3/retrieveAppointment/responses/CAAL.json"),
        ("70006", "stu3/retrieveAppointment/responses/Cancelled.json",),
        ("70007", "stu3/retrieveAppointment/responses/AandGConvertedToDBS.json"),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/Appointment/{id}/_history/{version}"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.GET

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestGetAppointment.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestGetAppointment.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_pathParams(
            actor, {"id": "70000", "version": "5"}, headers
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("id,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        id,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_pathParams(
            actor, {"id": id, "version": "5"}
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response, additional={"etag": 'W/"5"',},
        )
