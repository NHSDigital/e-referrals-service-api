import pytest
import requests


HEADER_AUTHORIZATION = 'Authorization'
HEADER_ECHO = 'echo' # enable echo target
HEADER_BASE_URL = 'x-ers-network-baseurl'
HEADER_USER_ID = 'x-ers-user-id'
HEADER_X_REQUEST_ID = 'x-request-id'
HEADER_ASID = 'xapi_asid'

CORRELATION_ID = "CORRELATION_ID"
BUSINESS_FUNCTION = "BUSINESS_FUNCTION"
ODS_CODE = "ODS_CODE"
FILENAME = "FILENAME"
COMM_RULE_ORG = "COMM_RULE_ORG"
REFERRAL_ID = "REFERRAL_ID"

EXPECTED_REFERRAL_ID = '000000040032'
EXPECTED_CORRELATION_ID = '123123-123123-123123-123123'
EXPECTED_BUSINESS_FUNCTION = 'REFERRING_CLINICIAN'
EXPECTED_ODS_CODE = 'R69'
EXPECTED_FILENAME = 'mysuperfilename.txt'
EXPECTED_ASID = '280477200122'
EXPECTED_COMM_RULE_ORG = 'R100'
EXPECTED_USERID = '0987654321123'

ORIGINAL_HEADERS = {
    CORRELATION_ID : "x-correlation-id",
    BUSINESS_FUNCTION: "nhsd-ers-business-function",
    ODS_CODE : "nhsd-ers-ods-code",
    FILENAME : "nhsd-ers-file-name",
    COMM_RULE_ORG : "nhsd-ers-comm-rule-org",
    REFERRAL_ID : "nhsd-ers-referral-id"
}

RENAMED_HEADERS = {
    CORRELATION_ID : "nhsd-correlation-id",
    BUSINESS_FUNCTION : "x-ers-business-function",
    ODS_CODE : "x-ers-ods-code",
    FILENAME : "x-ers-xapi-meta-file_name",
    COMM_RULE_ORG : "x-ers-xapi-comm-rule-org",
    REFERRAL_ID : "x-ers-xapi-meta-intended_ubrn"
}

@pytest.mark.integration_test
class TestHeaders:

    @pytest.mark.parametrize('user_id,asid', [(EXPECTED_USERID,EXPECTED_ASID)])
    def test_headers(self, access_code, service_url):
        client_request_headers = {
            HEADER_ECHO : '', # enable echo target
            HEADER_AUTHORIZATION : 'Bearer ' + access_code,
            HEADER_X_REQUEST_ID: 'DUMMY-VALUE',
            ORIGINAL_HEADERS[REFERRAL_ID] : EXPECTED_REFERRAL_ID,
            ORIGINAL_HEADERS[CORRELATION_ID] : EXPECTED_CORRELATION_ID,
            ORIGINAL_HEADERS[BUSINESS_FUNCTION] : EXPECTED_BUSINESS_FUNCTION,
            ORIGINAL_HEADERS[ODS_CODE] : EXPECTED_ODS_CODE,
            ORIGINAL_HEADERS[FILENAME] : EXPECTED_FILENAME,
            ORIGINAL_HEADERS[COMM_RULE_ORG] : EXPECTED_COMM_RULE_ORG}

        # Make the API call
        response = requests.get(service_url, headers=client_request_headers)
        assert response.status_code == 200, "Expected a 200 when accesing the api but got " + (str)(response.status_code)

        json_response = response.json()
        target_request_headers = json_response['headers']


        # Verify the header values
        for header in ORIGINAL_HEADERS:
            assert ORIGINAL_HEADERS[header] not in target_request_headers

        assert HEADER_X_REQUEST_ID not in target_request_headers

        for header in RENAMED_HEADERS:
            assert RENAMED_HEADERS[header] in target_request_headers

        assert target_request_headers[RENAMED_HEADERS[REFERRAL_ID]] == EXPECTED_REFERRAL_ID
        assert target_request_headers[RENAMED_HEADERS[CORRELATION_ID]].startswith(EXPECTED_CORRELATION_ID)
        assert target_request_headers[RENAMED_HEADERS[BUSINESS_FUNCTION]] == EXPECTED_BUSINESS_FUNCTION
        assert target_request_headers[RENAMED_HEADERS[ODS_CODE]] == EXPECTED_ODS_CODE
        assert target_request_headers[RENAMED_HEADERS[FILENAME]] == EXPECTED_FILENAME
        assert target_request_headers[RENAMED_HEADERS[COMM_RULE_ORG]] == EXPECTED_COMM_RULE_ORG

        assert target_request_headers[HEADER_ASID] == EXPECTED_ASID
        assert target_request_headers[HEADER_USER_ID] == EXPECTED_USERID
        assert target_request_headers[HEADER_BASE_URL] == service_url
