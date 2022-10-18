import pytest
import requests

from data import RenamedHeader
from asserts import assert_ok_response

_HEADER_AUTHORIZATION = "Authorization"
_HEADER_ECHO = "echo"  # enable echo target
_HEADER_BASE_URL = "x-ers-network-baseurl"
_HEADER_USER_ID = "x-ers-user-id"
_HEADER_REQUEST_ID = "x-request-id"
_HEADER_ASID = "xapi_asid"
_HEADER_ACCESS_MODE = "x-ers-access-mode"

_EXPECTED_REFERRAL_ID = "000000040032"
_EXPECTED_CORRELATION_ID = "123123-123123-123123-123123"
_EXPECTED_FILENAME = "mysuperfilename.txt"
_EXPECTED_COMM_RULE_ORG = "R100"
_EXPECTED_OBO_USER_ID = "0123456789000"
_EXPECTED_ACCESS_MODE = "user-restricted"

_SPECIALTY_REF_DATA_URL = "/FHIR/STU3/CodeSystem/SPECIALTY"
_SEARCH_HEALTHCARE_SERVICE_R4_URL = "/FHIR/R4/HealthcareService"


@pytest.mark.integration_test
class TestHeaders:
    @pytest.mark.asyncio
    async def test_headers_on_echo_target(
        self, authenticate_user, service_url, referring_clinician, asid
    ):
        access_code = await authenticate_user(referring_clinician)

        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            _HEADER_REQUEST_ID: "DUMMY-VALUE",
            RenamedHeader.REFERRAL_ID.original: _EXPECTED_REFERRAL_ID,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: referring_clinician.business_function,
            RenamedHeader.ODS_CODE.original: referring_clinician.org_code,
            RenamedHeader.FILENAME.original: _EXPECTED_FILENAME,
            RenamedHeader.COMM_RULE_ORG.original: _EXPECTED_COMM_RULE_ORG,
            RenamedHeader.OBO_USER_ID.original: _EXPECTED_OBO_USER_ID,
        }

        # Make the API call
        response = requests.get(service_url, headers=client_request_headers)
        assert (
            response.status_code == 200
        ), "Expected a 200 when accesing the api but got " + (str)(response.status_code)

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

        # Verify the headers are in or out
        for renamed_header in RenamedHeader:
            assert renamed_header.original not in target_request_headers
            assert renamed_header.renamed in target_request_headers

        assert _HEADER_REQUEST_ID not in target_request_headers

        # Verify the header values
        assert (
            target_request_headers[RenamedHeader.REFERRAL_ID.renamed]
            == _EXPECTED_REFERRAL_ID
        )
        assert target_request_headers[RenamedHeader.CORRELATION_ID.renamed].startswith(
            _EXPECTED_CORRELATION_ID
        )
        assert (
            target_request_headers[RenamedHeader.BUSINESS_FUNCTION.renamed]
            == referring_clinician.business_function
        )
        assert (
            target_request_headers[RenamedHeader.ODS_CODE.renamed]
            == referring_clinician.org_code
        )
        assert (
            target_request_headers[RenamedHeader.FILENAME.renamed] == _EXPECTED_FILENAME
        )
        assert (
            target_request_headers[RenamedHeader.COMM_RULE_ORG.renamed]
            == _EXPECTED_COMM_RULE_ORG
        )
        assert (
            target_request_headers[RenamedHeader.OBO_USER_ID.renamed]
            == _EXPECTED_OBO_USER_ID
        )

        assert target_request_headers[_HEADER_ASID] == asid
        assert target_request_headers[_HEADER_USER_ID] == referring_clinician.user_id
        assert target_request_headers[_HEADER_BASE_URL] == service_url
        assert target_request_headers[_HEADER_ACCESS_MODE] == _EXPECTED_ACCESS_MODE

    @pytest.mark.asyncio
    async def test_headers_on_refdata_response(
        self, authenticate_user, service_url, referring_clinician
    ):
        access_code = await authenticate_user(referring_clinician)

        client_request_headers = {
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: referring_clinician.business_function,
            RenamedHeader.ODS_CODE.original: referring_clinician.org_code,
            _HEADER_REQUEST_ID: "DUMMY",  # this must be less than 10 characters
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{_SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        assert_ok_response(response, _EXPECTED_CORRELATION_ID)

    @pytest.mark.parametrize(
        "auth_header,endpoint_url,is_operation_outcome",
        [
            ("Bearer 99999999999999999999999999999999", _SPECIALTY_REF_DATA_URL, False),
            (None, _SPECIALTY_REF_DATA_URL, False),
            ("", _SPECIALTY_REF_DATA_URL, False),
            ("Bearer ", _SPECIALTY_REF_DATA_URL, False),
            (
                "Bearer 99999999999999999999999999999999",
                _SEARCH_HEALTHCARE_SERVICE_R4_URL,
                True,
            ),
        ],
    )
    def test_unknown_access_code(
        self, service_url, auth_header, endpoint_url, is_operation_outcome
    ):
        client_request_headers = {
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            _HEADER_REQUEST_ID: "DUMMY",
        }

        if auth_header is not None:
            client_request_headers[_HEADER_AUTHORIZATION] = auth_header

        # Make the API call
        response = requests.get(
            f"{service_url}{endpoint_url}", headers=client_request_headers
        )

        # Verify the status
        assert (
            response.status_code == 401
        ), "Expected a 401 when accesing the api but got " + (str)(response.status_code)

        if not is_operation_outcome:
            assert len(response.content) == 0
        else:
            response_data = response.json()
            assert response_data["resourceType"] == "OperationOutcome"
            assert response_data["meta"]["lastUpdated"] is not None
            assert len(response_data["issue"]) == 1
            issue = response_data["issue"][0]
            assert issue["severity"] == "error"
            assert issue["code"] == "forbidden"
            assert issue["diagnostics"].lower() == "invalid access token"
            assert len(issue["details"]["coding"]) == 1
            issue_details = issue["details"]["coding"][0]
            assert (
                issue_details["system"]
                == "https://fhir.nhs.uk/CodeSystem/NHSD-API-ErrorOrWarningCode"
            )
            assert issue_details["code"] == "ACCESS_DENIED"

        # Verify the response headers
        client_response_headers = response.headers
        assert 'error="invalid_token"' in client_response_headers["WWW-Authenticate"]
        assert client_response_headers[_HEADER_REQUEST_ID] == "DUMMY"

        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == _EXPECTED_CORRELATION_ID
        )

        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers

    @pytest.mark.asyncio
    @pytest.mark.parametrize("service_name", [(None)])
    async def test_access_code_not_supported(
        self, referring_clinician, authenticate_user, service_url
    ):
        access_code = await authenticate_user(referring_clinician)

        client_request_headers = {
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            _HEADER_REQUEST_ID: "DUMMY",
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{_SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        # Verify the status
        assert (
            response.status_code == 401
        ), "Expected a 401 when accesing the api but got " + (str)(response.status_code)

        assert len(response.content) == 0

        # Verify the response headers
        client_response_headers = response.headers
        assert client_response_headers[_HEADER_REQUEST_ID] == "DUMMY"
        assert 'error="invalid_token"' in client_response_headers["WWW-Authenticate"]
        assert (
            "Invalid API call as no apiproduct match found"
            in client_response_headers["WWW-Authenticate"]
        )

        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == _EXPECTED_CORRELATION_ID
        )

        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers
