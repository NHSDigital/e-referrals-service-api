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

    valid_test_data = [
        (
            "att-70000-70001",
            "stu3/retrieveAttachment/responses/example_attachment.pdf",
            "example_attachment.pdf",
        ),
        (
            # Any arbitrary v4 UUID should work here
            "f1b1b2b1-30db-48f9-8906-8b703adca5fb",
            "stu3/retrieveAttachment/responses/example_attachment.pdf",
            "example_attachment.pdf",
        ),
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/Binary/{attachmentLogicalID}"

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
            actor, {"attachmentLogicalID": "att-70000-70001"}, headers
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("id,response, filename", valid_test_data)
    def test_success(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        load_file: Callable[[str], bytes],
        actor: Actor,
        id,
        response,
        filename,
    ):
        expected_response = load_file(response)
        actual_response = call_endpoint_url_with_pathParams(
            actor, {"attachmentLogicalID": id}
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_file_response(expected_response, actual_response)

        asserts.assert_file_response_headers(
            actual_response,
            additional={
                "content-disposition": "attachment; filename=" + filename,
                "content-length": str(len(expected_response)),
            },
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    def test_failure_not_a_uuid(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        actor: Actor,
    ):
        response = call_endpoint_url_with_pathParams(
            actor, {"attachmentLogicalID": "f1bb2b1-30db-48f9-8906-8b703adca5fb"}
        )
        asserts.assert_status_code(422, response.status_code)
