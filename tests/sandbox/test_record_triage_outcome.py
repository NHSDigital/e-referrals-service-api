from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestRecordTriageOutcome(SandboxTest):
    @pytest.fixture
    def unauthorised_actors(self) -> Iterable[Actor]:
        return self.unauthorised_actors_list()

    def unauthorised_actors_list(self) -> List[Actor]:
        return []

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
            "SERVICE_PROVIDER_CLINICIAN_ADMIN",
        ]

    @pytest.fixture
    def call_endpoint(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: send_rest_request(
            HttpMethod.POST,
            "FHIR/STU3/ReferralRequest/000000070000/$ers.recordReviewOutcome",
            actor,
            json=load_json(
                "recordTriageOutcome/requests/ReturnToReferrerWithAdvice.json"
            ),
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
            "FHIR/STU3/ReferralRequest/000000070000/$ers.recordReviewOutcome",
            actor,
            json=load_json(requestJson),
            headers=headers,
        )

    testdata = [
        (
            "recordTriageOutcome/requests/ReturnToReferrerWithAdvice.json",
            "recordTriageOutcome/responses/ReturnToReferrerWithAdvice.json",
        ),
        (
            "recordTriageOutcome/requests/AcceptReferBookLater.json",
            "recordTriageOutcome/responses/AcceptReferBookLater.json",
        ),
        (
            "recordTriageOutcome/requests/AttachmentIncluded.json",
            "recordTriageOutcome/responses/AttachmentIncluded.json",
        ),
    ]

    @pytest.mark.parametrize("actor", [Actor.SPC, Actor.SPCA])
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

        asserts.assert_headers(
            actual_response, additional={"etag": 'W/"10"',},
        )
