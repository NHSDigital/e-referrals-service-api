from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestSearchForHealthcareServices(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    testdata = [
        (
            "1,2",
            "searchForServices/responses/searchServiceWithMinmumalAttributes.json",
        ),
        (
            "3,4",
            "searchForServices/responses/searchServiceWithMaxAndMinlAttributes.json",
        ),
        ("5,6", "searchForServices/responses/searchServiceWithEmptyResponse.json",),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/R4/HealthcareService"

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestSearchForHealthcareServices.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestSearchForHealthcareServices.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_get_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_get_endpoint_url_with_query(
            actor, {"_id": "1,2"}, headers,
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("ids,response", testdata)
    def test_success(
        self,
        call_get_endpoint_url_with_query: Callable[[Actor, Dict[str, str]], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        ids,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_get_endpoint_url_with_query(actor, {"_id": ids})

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(actual_response,)
