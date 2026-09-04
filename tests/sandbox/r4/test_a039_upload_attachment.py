from typing import Callable, Dict, Iterable

import pytest
from tests import asserts

from requests import Response
from tests.sandbox.SandboxTest import SandboxTest
from tests.data import Actor, RenamedHeader
from tests.sandbox.utils import HttpMethod


@pytest.mark.sandbox
class TestUploadAttachmentR4(SandboxTest):
    allowed_business_function_data = [
        "REFERRING_CLINICIAN",
        "REFERRING_CLINICIAN_ADMIN",
        "SERVICE_PROVIDER_CLINICIAN",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
    ]

    authorised_actor_data = Actor.all(
        required_business_functions=allowed_business_function_data
    )

    @pytest.fixture
    def endpoint_url(self) -> str:
        return "FHIR/R4/Binary"

    @pytest.fixture
    def http_method(self) -> HttpMethod:
        return HttpMethod.POST

    @pytest.fixture
    def authorised_actors(self) -> Iterable[Actor]:
        return TestUploadAttachmentR4.authorised_actor_data

    @pytest.fixture
    def allowed_business_functions(self) -> Iterable[str]:
        return TestUploadAttachmentR4.allowed_business_function_data

    @pytest.fixture
    def default_headers(self) -> Dict[str, str]:
        return {
            RenamedHeader.FILENAME.original: "upload.txt",
            RenamedHeader.REFERRAL_ID.original: "000000070000",
            "nhsd-ers-file-size": "128",
            "nhsd-ers-file-mime-type": "text/plain",
            "content-type": "text/plain",
        }

    @pytest.fixture
    def call_endpoint(
        self,
        call_endpoint_url_with_file: Callable[[Actor, str, Dict[str, str]], Response],
    ) -> Callable[[Actor, Dict[str, str]], Response]:
        return lambda actor, headers={}: call_endpoint_url_with_file(
            actor,
            "r4/uploadFileToDocumentStore/requests/upload.txt",
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
    def test_success(
        self,
        call_endpoint_url_with_file: Callable[[Actor, str, Dict[str, str]], Response],
        load_json: Callable[[str], Dict[str, str]],
        sandbox_url: str,
        actor: Actor,
    ):
        headers = {
            RenamedHeader.FILENAME.original: "upload.txt",
            RenamedHeader.REFERRAL_ID.original: "000000070000",
            "nhsd-ers-file-size": "128",
            "nhsd-ers-file-mime-type": "text/plain",
            "content-type": "text/plain",
        }

        actual_response = call_endpoint_url_with_file(
            actor, "r4/uploadFileToDocumentStore/requests/upload.txt", headers
        )

        expected_response = load_json(
            "r4/uploadFileToDocumentStore/responses/BinaryResource.json"
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)
        asserts.assert_json_response_headers(
            actual_response,
            additional={
                "Location": f"{sandbox_url}/ObjectStore/d497bbe3-f88b-45f1-b3d4-9c563e4c0f5f",
                "Content-Disposition": "attachment; filename=\"upload.txt\"; filename*=UTF-8''upload.txt",
            },
        )

    @pytest.mark.parametrize("actor", authorised_actor_data)
    def test_success_without_payload(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
        http_method: HttpMethod,
        sandbox_url: str,
        actor: Actor,
    ):
        headers = {
            RenamedHeader.FILENAME.original: "upload.txt",
            RenamedHeader.REFERRAL_ID.original: "000000070000",
            "nhsd-ers-file-size": "128",
            "nhsd-ers-file-mime-type": "text/plain",
            "content-type": "text/plain",
        }

        actual_response = send_rest_request(
            http_method,
            endpoint_url,
            actor,
            headers=headers,
        )

        expected_response = load_json(
            "r4/uploadFileToDocumentStore/responses/BinaryResource.json"
        )

        asserts.assert_status_code(200, actual_response.status_code)
        asserts.assert_response(expected_response, actual_response)
        asserts.assert_json_response_headers(
            actual_response,
            additional={
                "Location": f"{sandbox_url}/ObjectStore/d497bbe3-f88b-45f1-b3d4-9c563e4c0f5f",
                "Content-Disposition": "attachment; filename=\"upload.txt\"; filename*=UTF-8''upload.txt",
            },
        )
