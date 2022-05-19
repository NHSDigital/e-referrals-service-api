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
    @pytest.fixture
    def unauthorised_actors(self) -> Iterable[Actor]:
        return self.unauthorised_actors_list()

    def unauthorised_actors_list(self) -> List[Actor]:
        return [Actor.RA, Actor.SPA]

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
            "REFERRING_CLINICIAN",
            "REFERRING_CLINICIAN_ADMIN",
            "SERVICE_PROVIDER_CLINICIAN",
            "SERVICE_PROVIDER_CLINICIAN_ADMIN",
        ]

    @pytest.fixture
    def call_endpoint(
        self, send_rest_request: Callable[[HttpMethod, str, Actor], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: send_rest_request(
            HttpMethod.GET, "FHIR/STU3/CodeSystem/SPECIALTY", actor, headers=headers
        )

    def test_success(
        self,
        call_endpoint: Callable[[Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        authorised_actors: Iterable[Actor],
    ):
        for actor in authorised_actors:
            actual_response = call_endpoint(actor)

            asserts.assert_status_code(200, actual_response.status_code)
            asserts.assert_response(
                load_json("getCodeSystem/responses/SpecialtyCodeSystem.json"),
                actual_response,
            )

            asserts.assert_headers(actual_response)
