from typing import Callable, Dict, Iterable
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestGetCodesystem(SandboxTest):
    @pytest.fixture
    def unauthorised_actors(self) -> Iterable[Actor]:
        return []

    @pytest.fixture
    def call_endpoint(
        self, send_rest_request: Callable[[HttpMethod, str, Actor], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: send_rest_request(
            HttpMethod.GET, "FHIR/STU3/CodeSystem/SPECIALTY", actor, headers=headers
        )

    @pytest.mark.parametrize("actor", Actor)
    def test_success(
        self,
        call_endpoint: Callable[[Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
    ):
        actual_response = call_endpoint(actor)

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(
            load_json("getCodeSystem/responses/SpecialtyCodeSystem.json"),
            actual_response,
        )

        asserts.assert_headers(actual_response)
