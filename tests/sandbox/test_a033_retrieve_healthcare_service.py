from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestRetrieveHealthcareService(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RC_DEV, Actor.RCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
    ]

    testdata = [
        ("1", "getService/responses/sampleServiceWithMinimumAttributes.json",),
        ("2", "getService/responses/sampleServiceWithFullAttributes.json",),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/R4/HealthcareService/{id}"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.GET

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestRetrieveHealthcareService.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestRetrieveHealthcareService.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_pathParams(
            actor, {"id": "1"}, headers
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("serviceId,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        serviceId,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_pathParams(actor, {"id": serviceId})

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response, additional={"etag": 'W/"1"',},
        )
