import pytest
import requests
from tests.data import RenamedHeader, Actor

_HEADER_AUTHORIZATION = "Authorization"
_HEADER_ECHO = "echo"  # enable echo target
_HEADER_BASE_URL = "x-ers-network-baseurl"
_HEADER_USER_ID = "x-ers-user-id"
_HEADER_REQUEST_ID = "x-request-id"
_HEADER_ASID = "xapi_asid"
_HEADER_ACCESS_MODE = "x-ers-access-mode"
_HEADER_AAL = "x-ers-authentication-assurance-level"
_HEADER_AMR = "x-ers-amr"
_HEADER_ID_ASSURANCE_LEVEL = "x-ers-id-assurance-level"

_EXPECTED_REFERRAL_ID = "000000040032"
_EXPECTED_CORRELATION_ID = "123123-123123-123123-123123"
_EXPECTED_FILENAME = "mysuperfilename.txt"
_EXPECTED_COMMA_FILENAME = "mysuper,filename.txt"
_EXPECTED_COMM_RULE_ORG = "R100"
_EXPECTED_OBO_USER_ID = "0123456789000"
_EXPECTED_ACCESS_MODE = "user-restricted"

_SPECIALTY_REF_DATA_URL = "/FHIR/STU3/CodeSystem/SPECIALTY"
_SEARCH_HEALTHCARE_SERVICE_R4_URL = "/FHIR/R4/HealthcareService"


@pytest.mark.integration_test
class TestUserRestricted:

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "endpoint_url, is_fhir_4, user",
        [
            ("", False, Actor.RC_DEV),
            ("/FHIR/R4/", True, Actor.RC_DEV),
            ("/FHIR/STU3/", False, Actor.RC_DEV),
        ],
    )
    async def test_user_restricted_valid_ods_code(
        self,
        authenticate_user,
        service_url,
        user: Actor,
        asid,
        endpoint_url,
        is_fhir_4,
    ):
        access_code = await authenticate_user(user)

        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            _HEADER_REQUEST_ID: "DUMMY-VALUE",
            RenamedHeader.REFERRAL_ID.original: _EXPECTED_REFERRAL_ID,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: user.business_function,
            RenamedHeader.ODS_CODE.original: user.org_code,
            RenamedHeader.FILENAME.original: _EXPECTED_FILENAME,
            RenamedHeader.COMM_RULE_ORG.original: _EXPECTED_COMM_RULE_ORG,
            RenamedHeader.OBO_USER_ID.original: _EXPECTED_OBO_USER_ID,
        }

        # Make the API call
        response = requests.get(
            f"{service_url}{endpoint_url}", headers=client_request_headers
        )

        # Verify the status
        assert (
            response.status_code == 200
        ), "Expected a 200 when accessing the api but got " + str(response.status_code)
