from typing import Callable, Dict, Iterable, List
from urllib import response

import pytest
import asserts

from requests import Response
from SandboxTest import SandboxTest
from data import Actor
from utils import HttpMethod


@pytest.mark.sandbox
class TestGetReferralWorklist(SandboxTest):
    @pytest.fixture
    def unauthorised_actors(self) -> Iterable[Actor]:
        return self.unauthorised_actors_list()

    def unauthorised_actors_list(self) -> List[Actor]:
        return []

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        authorised = []
        for actor in Actor:
            if actor not in self.unauthorised_actors_list():
                authorised.append(actor)
        return authorised

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return [
            "REFERRING_CLINICIAN",
            "REFERRING_CLINICIAN_ADMIN",
            "SERVICE_PROVIDER_CLINICIAN",
            "SERVICE_PROVIDER_CLINICIAN_ADMIN",
        ]

    @pytest.fixture
    def call_endpoint(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: send_rest_request(
            HttpMethod.GET,
            "FHIR/STU3/ReferralRequest/000000070000",
            actor,
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint_with_ubrn(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor, str], Response]:
        return lambda actor, ubrn, headers={}: send_rest_request(
            HttpMethod.GET, "FHIR/STU3/ReferralRequest/" + ubrn, actor, headers=headers,
        )

    @pytest.fixture
    def call_endpoint_with_ubrn_and_version(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor, str, str], Response]:
        return lambda actor, ubrn, version, headers={}: send_rest_request(
            HttpMethod.GET,
            "FHIR/STU3/ReferralRequest/" + ubrn + "/_history/" + version,
            actor,
            headers=headers,
        )

    testdata = [
        ("000000070000", "retrieveReferralRequest/responses/Unbooked.json",),
        ("000000070001", "retrieveReferralRequest/responses/BookedDBS.json",),
        ("000000070002", "retrieveReferralRequest/responses/BookedIBS.json",),
        ("000000070003", "retrieveReferralRequest/responses/DeferredToProvider.json",),
        (
            "000000070004",
            "retrieveReferralRequest/responses/ConvertedFromAdviceAndGuidance.json",
        ),
        ("000000070005", "retrieveReferralRequest/responses/WithRelatedReferral.json",),
        (
            "000000070011",
            "retrieveReferralRequest/responses/WithAdditionalRequirements.json",
        ),
    ]

    @pytest.mark.parametrize("actor", [Actor.RC, Actor.RCA, Actor.SPC, Actor.SPCA])
    @pytest.mark.parametrize("ubrn,response", testdata)
    def test_success(
        self,
        call_endpoint_with_ubrn: Callable[[Actor, str], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        ubrn,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_with_ubrn(actor, ubrn)

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_headers(
            actual_response, additional={"etag": 'W/"5"',},
        )

    @pytest.mark.parametrize("actor", [Actor.RC, Actor.RCA, Actor.SPC, Actor.SPCA])
    @pytest.mark.parametrize("ubrn,response", testdata)
    def test_success_versioned(
        self,
        call_endpoint_with_ubrn_and_version: Callable[[Actor, str, str], Response],
        load_json: Callable[[str], Dict[str, str]],
        actor: Actor,
        ubrn,
        response,
    ):
        expected_response = load_json(response)
        actual_response = call_endpoint_with_ubrn_and_version(actor, ubrn, "5")

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)

        asserts.assert_headers(
            actual_response, additional={"etag": 'W/"5"',},
        )
