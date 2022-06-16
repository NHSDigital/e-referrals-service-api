from typing import Callable, Dict, Iterable

import pytest
import asserts

from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod
from requests import Response


@pytest.mark.sandbox
class TestPatientServiceSearch(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    testdata = [
        (
            Actor.RC,
            "patientServiceSearch/requests/RcMinimal.json",
            "patientServiceSearch/responses/FetchServiceListWithMultipleServices.json",
        ),
        (
            Actor.RC,
            "patientServiceSearch/requests/RcSearchByClinicalTerm.json",
            "patientServiceSearch/responses/EmptyResponse.json",
        ),
        (
            Actor.RC,
            "patientServiceSearch/requests/RcSearchByNamedClinician.json",
            "patientServiceSearch/responses/FetchServiceListWithSingleService.json",
        ),
        (
            Actor.RCA,
            "patientServiceSearch/requests/RcaWithIWT.json",
            "patientServiceSearch/responses/FetchServiceListWithSingleService.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/HealthcareService/$ers.searchHealthcareServicesForPatient"

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestPatientServiceSearch.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestPatientServiceSearch.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_request: Callable[
            [Actor, str, Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_request(
            actor, self._request_path(actor), headers,
        )

    @pytest.mark.parametrize("actor, requestJson, response", testdata)
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

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)
        asserts.assert_json_response_headers(actual_response,)

    def _request_path(self, actor: Actor) -> str:
        path = (
            "patientServiceSearch/requests/RcaWithIWT.json"
            if actor == Actor.RCA
            else "patientServiceSearch/requests/RcMinimal.json"
        )
        return path
