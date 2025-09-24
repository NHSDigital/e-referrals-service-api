import pytest
import requests
from requests import Response
from tests.data import RenamedHeader, Actor, UserAuthenticationLevel
from tests.asserts import assert_ok_response

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
        "endpoint_url, is_fhir_4, user, apim_app_flow_vars ",
        [
            ("", False, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
            ("/FHIR/R4/", True, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
            ("/FHIR/STU3/", False, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
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
        apim_app_flow_vars,
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

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "endpoint_url, is_fhir_4, user ,apim_app_flow_vars",
        [
            ("", False, Actor.RC_DEV, ["invalid_code"]),
            ("/FHIR/R4/", True, Actor.RC_DEV, ["invalid_code"]),
            ("/FHIR/STU3/", False, Actor.RC_DEV, ["invalid_code"]),
        ],
    )
    async def test_user_restricted_invalid_ods_code(
        self,
        authenticate_user,
        service_url,
        user: Actor,
        asid,
        endpoint_url,
        is_fhir_4,
        apim_app_flow_vars,
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
            response.status_code == 403
        ), "Expected a 403 when accessing the api but got " + str(response.status_code)
        # Verify the OperationOutcome payload
        response_data = response.json()
        assert response_data["resourceType"] == "OperationOutcome"
        assert response_data["meta"]["lastUpdated"] is not None
        assert len(response_data["meta"]["profile"]) == 1
        assert response_data["meta"]["profile"][0] == (
            "https://www.hl7.org/fhir/R4/operationoutcome.html"
            if is_fhir_4
            else "https://fhir.nhs.uk/STU3/StructureDefinition/eRS-OperationOutcome-1"
        )
        assert len(response_data["issue"]) == 1
        issue = response_data["issue"][0]
        assert issue["severity"] == "error"
        assert issue["code"] == "forbidden" if is_fhir_4 else "forbidden"
        assert issue["diagnostics"] == (
            "Unauthorised ODS code provided in NHSD-End-User-Organisation-ODS header"
        )
        assert len(issue["details"]["coding"]) == 1
        issue_details = issue["details"]["coding"][0]
        assert (
            issue_details["system"]
            == "https://fhir.nhs.uk/CodeSystem/NHSD-API-ErrorOrWarningCode"
            if is_fhir_4
            else "https://fhir.nhs.uk/STU3/CodeSystem/eRS-APIErrorCode-1"
        )
        assert issue_details["code"] == "ACCESS_DENIED" if is_fhir_4 else "NO_ACCESS"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "endpoint_url, is_fhir_4, user ,apim_app_flow_vars",
        [
            ("", False, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
            ("/FHIR/R4/", True, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
            ("/FHIR/STU3/", False, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
        ],
    )
    async def test_user_restricted_missing_ods_header(
        self,
        authenticate_user,
        service_url,
        user: Actor,
        asid,
        endpoint_url,
        is_fhir_4,
        apim_app_flow_vars,
    ):
        access_code = await authenticate_user(user)

        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            _HEADER_REQUEST_ID: "DUMMY-VALUE",
            RenamedHeader.REFERRAL_ID.original: _EXPECTED_REFERRAL_ID,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: user.business_function,
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
            response.status_code == 400
        ), "Expected a 400 when accessing the api but got " + str(response.status_code)
        # Verify the OperationOutcome payload
        response_data = response.json()
        assert response_data["resourceType"] == "OperationOutcome"
        assert response_data["meta"]["lastUpdated"] is not None
        assert len(response_data["meta"]["profile"]) == 1
        assert response_data["meta"]["profile"][0] == (
            "https://www.hl7.org/fhir/R4/operationoutcome.html"
            if is_fhir_4
            else "https://fhir.nhs.uk/STU3/StructureDefinition/eRS-OperationOutcome-1"
        )
        assert len(response_data["issue"]) == 1
        issue = response_data["issue"][0]
        assert issue["severity"] == "error"
        assert issue["code"] == "required" if is_fhir_4 else "required"
        assert issue["diagnostics"] == (
            "Missing or Empty NHSD-End-User-Organisation-ODS header."
        )
        assert len(issue["details"]["coding"]) == 1
        issue_details = issue["details"]["coding"][0]
        assert (
            issue_details["system"]
            == "https://fhir.nhs.uk/CodeSystem/NHSD-API-ErrorOrWarningCode"
            if is_fhir_4
            else "https://fhir.nhs.uk/STU3/CodeSystem/eRS-APIErrorCode-1"
        )
        assert (
            issue_details["code"] == "MISSING_HEADER" if is_fhir_4 else "MISSING_HEADER"
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "endpoint_url, is_fhir_4, user ,apim_app_flow_vars",
        [
            ("", False, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
            ("/FHIR/R4/", True, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
            ("/FHIR/STU3/", False, Actor.RC_DEV, [Actor.RC_DEV.org_code]),
        ],
    )
    async def test_user_restricted_missing_ods_code(
        self,
        authenticate_user,
        service_url,
        user: Actor,
        asid,
        endpoint_url,
        is_fhir_4,
        apim_app_flow_vars,
    ):
        access_code = await authenticate_user(user)

        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            _HEADER_REQUEST_ID: "DUMMY-VALUE",
            RenamedHeader.REFERRAL_ID.original: _EXPECTED_REFERRAL_ID,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: user.business_function,
            RenamedHeader.ODS_CODE.original: "",
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
            response.status_code == 400
        ), "Expected a 400 when accessing the api but got " + str(response.status_code)
        # Verify the OperationOutcome payload
        response_data = response.json()
        assert response_data["resourceType"] == "OperationOutcome"
        assert response_data["meta"]["lastUpdated"] is not None
        assert len(response_data["meta"]["profile"]) == 1
        assert response_data["meta"]["profile"][0] == (
            "https://www.hl7.org/fhir/R4/operationoutcome.html"
            if is_fhir_4
            else "https://fhir.nhs.uk/STU3/StructureDefinition/eRS-OperationOutcome-1"
        )
        assert len(response_data["issue"]) == 1
        issue = response_data["issue"][0]
        assert issue["severity"] == "error"
        assert issue["code"] == "required" if is_fhir_4 else "required"
        assert issue["diagnostics"] == (
            "Missing or Empty NHSD-End-User-Organisation-ODS header."
        )
        assert len(issue["details"]["coding"]) == 1
        issue_details = issue["details"]["coding"][0]
        assert (
            issue_details["system"]
            == "https://fhir.nhs.uk/CodeSystem/NHSD-API-ErrorOrWarningCode"
            if is_fhir_4
            else "https://fhir.nhs.uk/STU3/CodeSystem/eRS-APIErrorCode-1"
        )
        assert (
            issue_details["code"] == "MISSING_HEADER" if is_fhir_4 else "MISSING_HEADER"
        )
