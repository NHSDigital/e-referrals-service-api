import sys
from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from pytest_check import check
from utils import HttpMethod


@pytest.mark.sandbox
class TestRetrieveAdviceAndGuidanceOverview(SandboxTest):
    authorised_actor_data = [Actor.RC, Actor.RCA, Actor.RC_DEV, Actor.SPC, Actor.SPCA]

    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    testdata = [
        (
            "000049146177",
            "retrieveAdviceAndGuidanceOverviewPdf/responses/000049146177_Advice_And_Guidance_20220610143044.pdf",
            "000049146177_Advice_And_Guidance_20220610143044.pdf",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/CommunicationRequest/{ubrn}/$ers.generateCRI"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestRetrieveAdviceAndGuidanceOverview.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestRetrieveAdviceAndGuidanceOverview.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_pathParams(
            actor, {"ubrn": "000049146177"}, headers
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("ubrn,response, filename", testdata)
    def test_success(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        load_file: Callable[[str], bytes],
        actor: Actor,
        ubrn,
        response,
        filename,
    ):

        expected_response = load_file(response)
        actual_response = call_endpoint_url_with_pathParams(actor, {"ubrn": ubrn})

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_file_response(expected_response, actual_response)

        asserts.assert_file_response_headers(
            actual_response,
            additional={
                "content-disposition": "attachment; filename=" + filename,
                "content-length": str(len(expected_response)),
            },
        )
