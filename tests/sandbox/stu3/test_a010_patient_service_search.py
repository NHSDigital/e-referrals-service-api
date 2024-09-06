from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod
from requests import Response


@pytest.mark.sandbox
class TestPatientServiceSearch(SandboxTest):
    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    testdata = [
        (
            Actor.RC,
            "stu3/patientServiceSearch/requests/RcMinimal.json",
            "stu3/patientServiceSearch/responses/FetchServiceListWithMultipleServices.json",
        ),
        (
            Actor.RC,
            "stu3/patientServiceSearch/requests/RcSearchByClinicalTerm.json",
            "stu3/patientServiceSearch/responses/EmptyResponse.json",
        ),
        (
            Actor.RC,
            "stu3/patientServiceSearch/requests/RcSearchByNamedClinician.json",
            "stu3/patientServiceSearch/responses/FetchServiceListWithSingleService.json",
        ),
        (
            Actor.RC,
            "stu3/patientServiceSearch/requests/RcSearchForAdviceService.json",
            "stu3/patientServiceSearch/responses/AdviceServiceSearch.json",
        ),
        (
            Actor.RCA,
            "stu3/patientServiceSearch/requests/RcaWithIWT.json",
            "stu3/patientServiceSearch/responses/FetchServiceListWithSingleService.json",
        ),
        (
            Actor.RC,
            "stu3/patientServiceSearch/requests/RcSearchWithCommissioningRuleOrganisation.json",
            "stu3/patientServiceSearch/responses/FetchServiceListWithMultipleServices.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/HealthcareService/$ers.searchHealthcareServicesForPatient"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

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
            actor,
            self._request_path(actor),
            headers,
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
        asserts.assert_json_response_headers(
            actual_response,
        )

    def _request_path(self, actor: Actor) -> str:
        path = (
            "stu3/patientServiceSearch/requests/RcaWithIWT.json"
            if actor == Actor.RCA
            else "stu3/patientServiceSearch/requests/RcMinimal.json"
        )
        return path
