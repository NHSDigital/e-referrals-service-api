import pytest
import requests
from requests import Response
from tests.data import RenamedHeader
from tests.asserts import (
    assert_ok_response,
    assert_error_response,
    assert_error_response_with_body,
)

_HEADER_AUTHORIZATION = "Authorization"
_HEADER_ECHO = "echo"  # enable echo target
_HEADER_BASE_URL = "x-ers-network-baseurl"
_HEADER_USER_ID = "x-ers-user-id"
_HEADER_REQUEST_ID = "x-request-id"
_HEADER_ASID = "xapi_asid"
_HEADER_ACCESS_MODE = "x-ers-access-mode"

_EXPECTED_CORRELATION_ID = "123123-123123-123123-123123"

_SPECIALTY_REF_DATA_URL = "/FHIR/STU3/CodeSystem/SPECIALTY"
_PROVIDER_AUTHORISED_APPLICATION = "PROVIDER_AUTHORISED_APPLICATION"
_REFERRER_AUTHORISED_APPLICATION = "REFERRER_AUTHORISED_APPLICATION"
_EXPECTED_ACCESS_MODE = "application-restricted"


@pytest.mark.integration_test
class TestAppRestricted:
    @pytest.mark.asyncio
    async def test_authorised_application_not_supported_for_user_restricted(
        self, authenticate_user, service_url, referring_clinician
    ):
        access_code = await authenticate_user(referring_clinician)

        # attempt to use REFERRER_AUTHORISED_APPLICATION with an RC
        client_request_headers = {
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: _REFERRER_AUTHORISED_APPLICATION,
            RenamedHeader.ODS_CODE.original: referring_clinician.org_code,
            _HEADER_REQUEST_ID: "DUMMY",  # this must be less than 10 characters
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{_SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        assert_error_response_with_body(response, _EXPECTED_CORRELATION_ID, 403)

    def test_authorised_application_supported_for_app_restricted(
        self, app_restricted_access_code, service_url
    ):
        client_request_headers = {
            _HEADER_AUTHORIZATION: "Bearer " + app_restricted_access_code,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            _HEADER_REQUEST_ID: "DUMMY",  # this must be less than 10 characters
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{_SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        assert_ok_response(response, _EXPECTED_CORRELATION_ID)

    @pytest.mark.parametrize(
        "header,value",
        [
            (RenamedHeader.ODS_CODE.renamed, "ABC"),
            (RenamedHeader.BUSINESS_FUNCTION.renamed, _PROVIDER_AUTHORISED_APPLICATION),
            (RenamedHeader.BUSINESS_FUNCTION.renamed, _REFERRER_AUTHORISED_APPLICATION),
            (_HEADER_USER_ID, "1"),
        ],
    )
    def test_authorised_application_header_rejected(
        self, app_restricted_access_code, service_url, header, value
    ):
        client_request_headers = {
            _HEADER_AUTHORIZATION: "Bearer " + app_restricted_access_code,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            header: value,
            _HEADER_REQUEST_ID: "DUMMY",  # this must be less than 10 characters
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{_SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        assert_error_response(response, _EXPECTED_CORRELATION_ID, 403)

    def test_headers_on_echo_target(
        self,
        app_restricted_access_code,
        service_url,
        asid,
        app_restricted_ods_code,
        app_restricted_user_id,
        app_restricted_business_function,
    ):
        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + app_restricted_access_code,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            _HEADER_REQUEST_ID: "DUMMY",  # this must be less than 10 characters
        }

        # Make the API call
        response = requests.get(service_url, headers=client_request_headers)
        self.assert_ok_echo_response(
            response,
            service_url,
            asid,
            app_restricted_ods_code,
            app_restricted_user_id,
            app_restricted_business_function,
        )

    def assert_ok_echo_response(
        self,
        response: Response,
        service_url,
        asid,
        app_restricted_ods_code,
        app_restricted_user_id,
        app_restricted_business_function,
    ):
        assert (
            response.status_code == 200
        ), "Expected a 200 when accessing the api but got " + (str)(
            response.status_code
        )

        # Verify the response headers
        client_response_headers = response.headers
        assert _HEADER_REQUEST_ID not in client_response_headers
        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == _EXPECTED_CORRELATION_ID
        )

        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers

        # Verify the received headers by the target
        json_response = response.json()
        target_request_headers = json_response["headers"]

        expected_app_restricted_renamed_headers = [
            RenamedHeader.CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION,
            RenamedHeader.ODS_CODE,
        ]
        not_expected_renamed_headers = []
        for renamed_header in RenamedHeader:
            if renamed_header not in expected_app_restricted_renamed_headers:
                not_expected_renamed_headers.append(renamed_header)

        for renamed_header in RenamedHeader:
            assert renamed_header.original not in target_request_headers, (
                "Should not have any original headers in " + target_request_headers
            )
        assert _HEADER_REQUEST_ID not in target_request_headers, (
            "Should not have "
            + _HEADER_REQUEST_ID
            + " header in "
            + target_request_headers
        )

        for renamed_header in not_expected_renamed_headers:
            assert renamed_header.renamed not in target_request_headers, (
                "Should not have "
                + not_expected_renamed_headers
                + " renamed headers in "
                + target_request_headers
            )

        for renamed_header in expected_app_restricted_renamed_headers:
            assert renamed_header.renamed in target_request_headers, (
                "Should have "
                + expected_app_restricted_renamed_headers
                + " headers in "
                + target_request_headers
            )
        assert _HEADER_USER_ID in target_request_headers, (
            "Should have " + _HEADER_USER_ID + " header in " + target_request_headers
        )

        # Verify the header values
        assert target_request_headers[RenamedHeader.CORRELATION_ID.renamed].startswith(
            _EXPECTED_CORRELATION_ID
        )
        assert (
            target_request_headers[RenamedHeader.BUSINESS_FUNCTION.renamed]
            == app_restricted_business_function
        )
        assert (
            target_request_headers[RenamedHeader.ODS_CODE.renamed]
            == app_restricted_ods_code
        )
        assert target_request_headers[_HEADER_ASID] == asid
        assert target_request_headers[_HEADER_USER_ID] == app_restricted_user_id
        assert target_request_headers[_HEADER_BASE_URL] == service_url
        assert target_request_headers[_HEADER_ACCESS_MODE] == _EXPECTED_ACCESS_MODE

    def test_access_mode_header_overwritten_on_echo_target(
        self,
        app_restricted_access_code,
        service_url,
        asid,
        app_restricted_ods_code,
        app_restricted_user_id,
        app_restricted_business_function,
    ):
        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + app_restricted_access_code,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            _HEADER_REQUEST_ID: "DUMMY",  # this must be less than 10 characters
            _HEADER_ACCESS_MODE: "unknown-access-mode",
        }

        # Make the API call
        response = requests.get(service_url, headers=client_request_headers)
        self.assert_ok_echo_response(
            response,
            service_url,
            asid,
            app_restricted_ods_code,
            app_restricted_user_id,
            app_restricted_business_function,
        )
