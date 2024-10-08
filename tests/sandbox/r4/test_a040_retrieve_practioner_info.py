from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestRetrieveERSBusinessFunctions(SandboxTest):
    authorised_actor_data = [
        Actor.SPCA,
    ]

    allowed_business_function_data = ["SERVICE_PROVIDER_CLINICIAN_ADMIN"]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/R4/Practitioner"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.GET

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestRetrieveERSBusinessFunctions.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestRetrieveERSBusinessFunctions.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_query(
            actor,
            {"_query": "onBehalfOf"},
            headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    def test_success(
        self,
        call_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
    ):
        expected_response = load_json(
            "r4/retrieveOboUsers/responses/PractitionerBundle.json"
        )
        actual_response = call_endpoint_url_with_query(actor, {"_query": "onBehalfOf"})

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response,
        )
