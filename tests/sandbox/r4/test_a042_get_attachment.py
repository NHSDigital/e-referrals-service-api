from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestGetAttachment(SandboxTest):
    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    testdata = [("att-70000-70001"), ("c5d2d200-7613-4a69-9c5f-1bb68e04b8d8")]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/R4/Binary/{binaryId}"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.GET

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestGetAttachment.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestGetAttachment.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_pathParams(
            actor, {"binaryId": "att-70000-70001"}, headers
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("id", testdata)
    def test_success(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        actor: Actor,
        id: str,
        sandbox_url: str,
        environment: str,
    ):
        request_headers = (
            {"x-ers-sandbox-baseurl": sandbox_url} if environment == "local" else {}
        )

        actual_response = call_endpoint_url_with_pathParams(
            actor, {"binaryId": id}, request_headers
        )

        asserts.assert_status_code(307, actual_response.status_code)

        expected_headers = {
            "Location": sandbox_url
            + "/ObjectStore/d497bbe3-f88b-45f1-b3d4-9c563e4c0f5f",
            "x-request-id": "58621d65-d5ad-4c3a-959f-0438e355990e-1",
            "vary": "origin",
            "cache-control": "no-cache",
            "content-length": "0",
            "connection": "keep-alive",
            "access-control-expose-headers": "x-correlation-id,x-request-id,content-type,Location,ETag,Content-Disposition,Content-Length,Cache-Control",
        }

        asserts.assert_response_headers(
            actual_response,
            expected_headers,
            assert_content_length=True,
            assert_ignored_headers=False,
        )

    def test_sandbox_error(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        load_json: Callable[[str], Dict[str, str]],
    ):
        expected_response = load_json("r4/R4-SandboxErrorOutcome.json")

        actual_response = call_endpoint_url_with_pathParams(
            Actor.RC, {"binaryId": "invalidBinaryId"}
        )

        asserts.assert_status_code(400, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)
