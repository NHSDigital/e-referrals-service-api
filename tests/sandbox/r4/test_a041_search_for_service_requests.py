from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestSearchForServiceRequests(SandboxTest):
    authorised_actor_data = [
        Actor.RC,
        Actor.RCA,
        Actor.RC_DEV,
        Actor.RC_INSUFFICIENT_IAL,
        Actor.SPC,
        Actor.SPCA,
    ]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    testdata = [
        (
            "000000070000",
            "r4/searchServiceRequest/responses/ResponseExampleReferral.json",
        ),
        (
            "000000070001",
            "r4/searchServiceRequest/responses/ResponseExampleAdvice.json",
        ),
        (
            "000000070002",
            "r4/searchServiceRequest/responses/ResponseExampleReferralAndAdvice.json",
        ),
        (
            "000000070003",
            "r4/searchServiceRequest/responses/ResponseExampleEmpty.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/R4/ServiceRequest"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.GET

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestSearchForServiceRequests.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestSearchForServiceRequests.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_query(
            actor,
            {"identifier": "000000070000"},
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("identifier,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        identifier,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_query(
            actor, {"identifier": identifier}
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response,
        )
