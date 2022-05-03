from typing import Callable, Dict, Iterable

import pytest
import asserts

from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod
from requests import Response


@pytest.mark.sandbox
class TestCreateReferral(SandboxTest):
    @pytest.fixture
    def unauthorised_actors(self) -> Iterable[Actor]:
        return [Actor.SPC, Actor.SPCA, Actor.AA]

    @pytest.fixture
    def call_endpoint(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: send_rest_request(
            HttpMethod.POST,
            "FHIR/STU3/ReferralRequest/$ers.createReferral",
            actor,
            json=self._load_json_data(actor, load_json),
            headers=headers,
        )

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

    @pytest.mark.parametrize("actor", [Actor.RC, Actor.RCA])
    def test_success(
        self,
        call_endpoint: Callable[[Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
    ):
        expected_response = load_json("createReferral/responses/ReferralRequest.json")
        actual_response = call_endpoint(actor)

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
