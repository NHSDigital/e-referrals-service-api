from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor, RenamedHeader
from tests.sandbox.utils import HttpMethod
from pytest_check import check


@pytest.mark.sandbox
class TestGetAttachmentFollowRedirection(SandboxTest):
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
        return TestGetAttachmentFollowRedirection.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestGetAttachmentFollowRedirection.allowed_business_function_data

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
    ) -> Callable[[Actor], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_pathParams(
            actor, {"binaryId": "att-70000-70001"}, headers, allow_redirects=True
        )

    @pytest.fixture
    def follow_redirects(follow: bool) -> bool:
        """Provides a value overriding the default follow redirect behaviour."""
        return True

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("id", testdata)
    def test_success(
        self,
        call_endpoint_url_with_pathParams: Callable[
            [Actor, Dict[str, str], Dict[str, str]], Response
        ],
        actor: Actor,
        id: str,
    ):
        actual_response = call_endpoint_url_with_pathParams(
            actor, {"binaryId": id}, allow_redirects=True
        )

        asserts.assert_status_code(200, actual_response.status_code)

        expected_headers = {
            "content-disposition": """attachment; filename="=?UTF-8?Q?The_filenam=C3=A9.pdf?="; filename*=UTF-8''The%20filenam%C3%A9.pdf""",
            "content-type": "application/pdf",
            "content-length": "23681",
            "vary": "origin",
            "access-control-expose-headers": "x-correlation-id,x-request-id,content-type,Location,ETag,Content-Disposition,Content-Length,Cache-Control",
            "cache-control": "no-cache",
            "accept-ranges": "bytes",
            "Connection": "keep-alive",
        }

        asserts.assert_response_headers(
            actual_response,
            expected_headers,
            assert_content_length=True,
            assert_ignored_headers=False,
        )
