from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestUpdateAppointment(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]
    testdata = [
        (
            "updateAppointment/requests/MinimalCancellationReasonOnlyCommentNotMandatory.json",
            "updateAppointment/responses/MinimalCancellationReasonOnlyCommentNotMandatory.json",
            200,
        ),
        (
            "updateAppointment/requests/CancellationReasonAndMandatoryComment.json",
            "updateAppointment/responses/CancellationReasonAndMandatoryComment.json",
            200,
        ),
        (
            "updateAppointment/requests/CancellationReasonOnlyCommentMandatory.json",
            "updateAppointment/responses/CancellationReasonOnlyCommentMandatory.json",
            422,
        ),
        (
            "updateAppointment/requests/CancellationInvalidReason.json",
            "updateAppointment/responses/CancellationInvalidReason.json",
            422,
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/Appointment/70000"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.PUT

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestUpdateAppointment.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestUpdateAppointment.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self, call_endpoint_url_with_request: Callable[[Actor, str], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor,
            "updateAppointment/requests/MinimalCancellationReasonOnlyCommentNotMandatory.json",
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("requestJson,response,responseCode", testdata)
    def test_success(
        self,
        call_endpoint_url_with_request: Callable[[Actor, str], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        requestJson,
        response,
        responseCode,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_request(actor, requestJson)

        asserts.assert_status_code(responseCode, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response, additional={"etag": 'W/"5"',},
        )
