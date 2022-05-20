import pytest
import requests
from data import Actor, RenamedHeader
from asserts import assert_ok_response

_HEADER_AUTHORIZATION = "Authorization"
_HEADER_ECHO = "echo"  # enable echo target
_HEADER_BASE_URL = "x-ers-network-baseurl"
_HEADER_USER_ID = "x-ers-user-id"
_HEADER_REQUEST_ID = "x-request-id"
_HEADER_ASID = "xapi_asid"
_HEADER_ERS_TRANSACTION_ID = "X_ERS_TRANSACTION_ID"

_EXPECTED_REFERRAL_ID = "000000040032"
_EXPECTED_CORRELATION_ID = "123123-123123-123123-123123"
_EXPECTED_FILENAME = "mysuperfilename.txt"
_EXPECTED_ASID = "280477200122"
_EXPECTED_COMM_RULE_ORG = "R100"
_EXPECTED_ACTOR = Actor.RC
_EXPECTED_OBO_USER_ID = "0123456789000"

_SPECIALTY_REF_DATA_URL = "/FHIR/STU3/CodeSystem/SPECIALTY"


@pytest.mark.integration_test
class TestHeaders:
    @pytest.mark.parametrize("actor,asid", [(_EXPECTED_ACTOR, _EXPECTED_ASID)])
    def test_headers_on_echo_target(
        self, user_restricted_access_code, service_url, actor
    ):
        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + user_restricted_access_code,
            _HEADER_REQUEST_ID: "DUMMY-VALUE",
            RenamedHeader.REFERRAL_ID.original: _EXPECTED_REFERRAL_ID,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: actor.business_function,
            RenamedHeader.ODS_CODE.original: actor.org_code,
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
            == actor.business_function
        )
        assert target_request_headers[RenamedHeader.ODS_CODE.renamed] == actor.org_code
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

        assert target_request_headers[_HEADER_ASID] == _EXPECTED_ASID
        assert target_request_headers[_HEADER_USER_ID] == actor.user_id
        assert target_request_headers[_HEADER_BASE_URL] == service_url

    @pytest.mark.parametrize("actor", [(_EXPECTED_ACTOR)])
    def test_headers_on_refdata_response(
        self, user_restricted_access_code, service_url, actor
    ):
        client_request_headers = {
            _HEADER_AUTHORIZATION: "Bearer " + user_restricted_access_code,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: actor.business_function,
            RenamedHeader.ODS_CODE.original: actor.org_code,
            _HEADER_REQUEST_ID: "DUMMY",  # this must be less than 10 characters
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{_SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        assert_ok_response(response, _EXPECTED_CORRELATION_ID)

    @pytest.mark.parametrize(
        "auth_header",
        [("Bearer 99999999999999999999999999999999"), (None), (""), ("Bearer ")],
    )
    def test_unknown_access_code(self, service_url, auth_header):
        client_request_headers = {
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            _HEADER_REQUEST_ID: "DUMMY",
        }

        if auth_header is not None:
            client_request_headers[_HEADER_AUTHORIZATION] = auth_header

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
        assert 'error="invalid_token"' in client_response_headers["WWW-Authenticate"]
        assert client_response_headers[_HEADER_REQUEST_ID] == "DUMMY"

        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == _EXPECTED_CORRELATION_ID
        )

        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers

    @pytest.mark.parametrize("service_name,actor", [(None, _EXPECTED_ACTOR)])
    def test_access_code_not_supported(self, user_restricted_access_code, service_url):
        client_request_headers = {
            _HEADER_AUTHORIZATION: "Bearer " + user_restricted_access_code,
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
