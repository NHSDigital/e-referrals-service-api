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
    authorised_actor_data = [
        Actor.RC,
        Actor.RC_DEV,
        Actor.RC_INSUFFICIENT_IAL,
        Actor.RCA,
    ]

    allowed_business_function_data = [""]

    testdata = [
        (
            "1",
            "r4/getService/responses/sampleServiceWithMinimumAttributes.json",
        ),
        (
            "2",
            "r4/getService/responses/sampleServiceWithFullAttributes.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/R4/HealthcareService/{id}"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.HEAD

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
    def test_success(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        actor: Actor,
    ):
        actual_response = call_endpoint_url_with_pathParams(actor, {"id": "1"})

        asserts.assert_status_code(200, actual_response.status_code)

        asserts.assert_json_response_headers(
            actual_response,
            additional={
                "etag": 'W/"1"',
            },
        )
