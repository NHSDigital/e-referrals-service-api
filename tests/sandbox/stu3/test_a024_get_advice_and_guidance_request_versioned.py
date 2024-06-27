from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestGetAdviceAndGuidanceRequest(SandboxTest):

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
            "stu3/retrieveAdviceAndGuidanceRequest/responses/MinimalExample.json",
        ),
        (
            "000000070001",
            "stu3/retrieveAdviceAndGuidanceRequest/responses/WithAttachmentFileReference.json",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/CommunicationRequest/{ubrn}/_history/{version}"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.GET

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestGetAdviceAndGuidanceRequest.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestGetAdviceAndGuidanceRequest.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_pathParams(
            actor, {"ubrn": "000000070000", "version": "5"}, headers
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("ubrn,response", testdata)
    def test_success(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        ubrn,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_url_with_pathParams(
            actor, {"ubrn": ubrn, "version": "5"}
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_json_response_headers(
            actual_response,
            additional={
                "etag": 'W/"5"',
            },
        )
