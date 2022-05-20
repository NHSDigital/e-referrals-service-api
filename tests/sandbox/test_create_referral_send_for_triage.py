from typing import Callable, Dict, Iterable

import pytest
import asserts

from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod
from requests import Response


@pytest.mark.sandbox
class TestCreateReferralSendForTriage(SandboxTest):
    @pytest.fixture
    def unauthorised_actors(self) -> Iterable[Actor]:
        return [Actor.SPC, Actor.SPCA]

    @pytest.fixture
    def call_endpoint_with_request(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor, str], Response]:
        return lambda actor, requestJson, headers={}: send_rest_request(
            HttpMethod.POST,
            "FHIR/STU3/ReferralRequest/$ers.createReferralAndSendForTriage",
            actor,
            json=load_json(requestJson),
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: send_rest_request(
            HttpMethod.POST,
            "FHIR/STU3/ReferralRequest/$ers.createReferralAndSendForTriage",
            actor,
            json=self._load_json_data(actor, load_json),
            headers=headers,
        )

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

    testdata = [
        (
            Actor.RC,
            "createReferralAndSendForTriage/requests/Parameters.json",
            "createReferralAndSendForTriage/responses/ReferralRequest.json",
        ),
        (
            Actor.RCA,
            "createReferralAndSendForTriage/requests/ParametersWithNamedClinician.json",
            "createReferralAndSendForTriage/responses/ReferralRequestWithNamedClinician.json",
        ),
    ]

    @pytest.mark.parametrize("actor, requestJson, response", testdata)
    def test_success(
        self,
        call_endpoint_with_request: Callable[[Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        requestJson,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_with_request(actor, requestJson)

        asserts.assert_status_code(201, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)
        asserts.assert_headers(
            actual_response, additional={"etag": 'W/"1"',},
        )

    def _load_json_data(
        self, actor: Actor, load_json: Callable[[str], Dict[str, str]]
    ) -> Dict[str, str]:
        path = (
            "createReferral/requests/MinimalRequestWithReferringClinician.json"
            if actor == Actor.RCA
            else "createReferral/requests/MinimalRequest.json"
        )
        return load_json(path)
