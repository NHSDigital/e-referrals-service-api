import pytest
import requests
from data import Actor, RenamedHeader

HEADER_AUTHORIZATION = "Authorization"
HEADER_ECHO = "echo"  # enable echo target
HEADER_BASE_URL = "x-ers-network-baseurl"
HEADER_USER_ID = "x-ers-user-id"
HEADER_REQUEST_ID = "x-request-id"
HEADER_ASID = "xapi_asid"
HEADER_ERS_TRANSACTION_ID = "X_ERS_TRANSACTION_ID"

EXPECTED_REFERRAL_ID = "000000040032"
EXPECTED_CORRELATION_ID = "123123-123123-123123-123123"
EXPECTED_FILENAME = "mysuperfilename.txt"
EXPECTED_ASID = "280477200122"
EXPECTED_COMM_RULE_ORG = "R100"
EXPECTED_ACTOR = Actor.RC
EXPECTED_OBO_USER_ID = "0123456789000"

SPECIALTY_REF_DATA_URL = "/FHIR/STU3/CodeSystem/SPECIALTY"


@pytest.mark.integration_test
class TestHeaders:
    @pytest.mark.parametrize("actor,asid", [(EXPECTED_ACTOR, EXPECTED_ASID)])
    def test_headers_on_echo_target(self, access_code, service_url, actor):
        client_request_headers = {
            HEADER_ECHO: "",  # enable echo target
            HEADER_AUTHORIZATION: "Bearer " + access_code,
            HEADER_REQUEST_ID: "DUMMY-VALUE",
            RenamedHeader.REFERRAL_ID.original: EXPECTED_REFERRAL_ID,
            RenamedHeader.CORRELATION_ID.original: EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: actor.business_function,
            RenamedHeader.ODS_CODE.original: actor.org_code,
            RenamedHeader.FILENAME.original: EXPECTED_FILENAME,
            RenamedHeader.COMM_RULE_ORG.original: EXPECTED_COMM_RULE_ORG,
            RenamedHeader.OBO_USER_ID.original: EXPECTED_OBO_USER_ID,
        }

        # Make the API call
        response = requests.get(service_url, headers=client_request_headers)
        assert (
            response.status_code == 200
        ), "Expected a 200 when accesing the api but got " + (str)(response.status_code)

        # Verify the response headers
        client_response_headers = response.headers
        assert HEADER_REQUEST_ID not in client_response_headers
        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == EXPECTED_CORRELATION_ID
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

        assert HEADER_REQUEST_ID not in target_request_headers

        # Verify the header values
        assert (
            target_request_headers[RenamedHeader.REFERRAL_ID.renamed]
            == EXPECTED_REFERRAL_ID
        )
        assert target_request_headers[RenamedHeader.CORRELATION_ID.renamed].startswith(
            EXPECTED_CORRELATION_ID
        )
        assert (
            target_request_headers[RenamedHeader.BUSINESS_FUNCTION.renamed]
            == actor.business_function
        )
        assert target_request_headers[RenamedHeader.ODS_CODE.renamed] == actor.org_code
        assert (
            target_request_headers[RenamedHeader.FILENAME.renamed] == EXPECTED_FILENAME
        )
        assert (
            target_request_headers[RenamedHeader.COMM_RULE_ORG.renamed]
            == EXPECTED_COMM_RULE_ORG
        )
        assert (
            target_request_headers[RenamedHeader.OBO_USER_ID.renamed]
            == EXPECTED_OBO_USER_ID
        )

        assert target_request_headers[HEADER_ASID] == EXPECTED_ASID
        assert target_request_headers[HEADER_USER_ID] == actor.user_id
        assert target_request_headers[HEADER_BASE_URL] == service_url

    @pytest.mark.parametrize("actor", [(EXPECTED_ACTOR)])
    def test_headers_on_refdata_response(self, access_code, service_url, actor):
        client_request_headers = {
            HEADER_AUTHORIZATION: "Bearer " + access_code,
            RenamedHeader.CORRELATION_ID.original: EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: actor.business_function,
            RenamedHeader.ODS_CODE.original: actor.org_code,
            HEADER_REQUEST_ID: "DUMMY",  # this must be less than 10 characters
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        # Verify the status
        assert (
            response.status_code == 200
        ), "Expected a 200 when accesing the api but got " + (str)(response.status_code)

        # Verify the response headers
        client_response_headers = response.headers
        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == EXPECTED_CORRELATION_ID
        )
        assert len(client_response_headers[HEADER_REQUEST_ID]) > 10
        assert HEADER_ERS_TRANSACTION_ID not in client_response_headers

        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers

    @pytest.mark.parametrize(
        "auth_header",
        [("Bearer 99999999999999999999999999999999"), (None), (""), ("Bearer ")],
    )
    def test_unknown_access_code(self, service_url, auth_header):
        client_request_headers = {
            RenamedHeader.CORRELATION_ID.original: EXPECTED_CORRELATION_ID,
            HEADER_REQUEST_ID: "DUMMY",
        }

        if auth_header is not None:
            client_request_headers[HEADER_AUTHORIZATION] = auth_header

        # Make the API call
        response = requests.get(
            f"{service_url}{SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        # Verify the status
        assert (
            response.status_code == 401
        ), "Expected a 401 when accesing the api but got " + (str)(response.status_code)

        assert len(response.content) == 0

        # Verify the response headers
        client_response_headers = response.headers
        assert 'error="invalid_token"' in client_response_headers["WWW-Authenticate"]
        assert client_response_headers[HEADER_REQUEST_ID] == "DUMMY"

        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == EXPECTED_CORRELATION_ID
        )

        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers

    @pytest.mark.parametrize("service_name,actor", [(None, EXPECTED_ACTOR)])
    def test_access_code_not_supported(self, access_code, service_url):
        client_request_headers = {
            HEADER_AUTHORIZATION: "Bearer " + access_code,
            RenamedHeader.CORRELATION_ID.original: EXPECTED_CORRELATION_ID,
            HEADER_REQUEST_ID: "DUMMY",
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{SPECIALTY_REF_DATA_URL}", headers=client_request_headers
        )

        # Verify the status
        assert (
            response.status_code == 401
        ), "Expected a 401 when accesing the api but got " + (str)(response.status_code)

        assert len(response.content) == 0

        # Verify the response headers
        client_response_headers = response.headers
        assert client_response_headers[HEADER_REQUEST_ID] == "DUMMY"
        assert 'error="invalid_token"' in client_response_headers["WWW-Authenticate"]
        assert (
            "Invalid API call as no apiproduct match found"
            in client_response_headers["WWW-Authenticate"]
        )

        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == EXPECTED_CORRELATION_ID
        )

        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers
