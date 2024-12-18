from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor, RenamedHeader
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestUploadAttachment(SandboxTest):
    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    testdata = [
        "text/plain",
        "application/pdf",
        "text/xml",
        "text/rtf",
        "audio/basic",
        "audio/mpeg",
        "image/png",
        "image/gif",
        "image/jpeg",
        "image/tiff",
        "video/mpeg",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/dicom",
    ]

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/STU3/Binary"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestUploadAttachment.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestUploadAttachment.allowed_business_function_data

    @pytest.fixture
    def default_headers(self) -> Dict[str, str]:
        return {
            RenamedHeader.FILENAME.original: "upload.txt",
            RenamedHeader.REFERRAL_ID.original: "000000070000",
            "content-type": "text/plain",
        }

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_file: Callable[[Actor, str, Dict[str, str]], Response],
        default_headers: Dict[str, str],
    ) -> Callable[[Actor, Dict[str, str]], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_file(
            actor,
            "stu3/uploadFileToDocumentStore/requests/upload.txt",
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint_url_with_file(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_file: Callable[[str], bytes],
        endpoint_url: str,
        http_method: HttpMethod,
    ) -> Callable[[Actor, str], Response]:
        return lambda actor, file, headers={}: send_rest_request(
            http_method,
            endpoint_url,
            actor,
            headers=headers,
            data=load_file(file),
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    @pytest.mark.parametrize("contentType", testdata)
    def test_success(
        self,
        call_endpoint_url_with_file: Callable[[Actor, str, Dict[str, str]], Response],
        actor,
        contentType,
    ):
        headers = {
            RenamedHeader.FILENAME.original: "upload.txt",
            RenamedHeader.REFERRAL_ID.original: "000000070000",
            "content-type": contentType,
        }

        actual_response = call_endpoint_url_with_file(
            actor, "stu3/uploadFileToDocumentStore/requests/upload.txt", headers
        )

        asserts.assert_status_code(201, actual_response.status_code)

        expected_headers = {
            "content-type": "text/html; charset=utf-8",
            "x-request-id": "58621d65-d5ad-4c3a-959f-0438e355990e-1",
            "vary": "origin",
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "content-length": "0",
            "access-control-expose-headers": "x-correlation-id,x-request-id,content-type,Location,ETag,Content-Disposition,Content-Length,Cache-Control",
        }

        asserts.assert_response_headers(
            actual_response,
            expected_headers,
            additional={
                "Location": "Binary/19eb7224-dff3-4730-a5cb-67eac811f1a5",
            },
            assert_content_length=False,
            assert_ignored_headers=False,
        )
