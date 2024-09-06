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
class TestHeaders:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user", [Actor.RC, Actor.AAL2_USER])
    async def test_headers_on_echo_target(
        self, authenticate_user, service_url, user: Actor, asid
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
        response = requests.get(service_url, headers=client_request_headers)

        expected_aal = (
            "3"
            if user.authentication_assurance_level == UserAuthenticationLevel.AAL3
            else "2"
        )
        expected_amr = (
            "[N3_SMARTCARD]"
            if user.authentication_assurance_level == UserAuthenticationLevel.AAL3
            else "[TOTP]"
        )

        self.assert_ok_echo_response(
            response,
            service_url,
            user,
            asid,
            _EXPECTED_FILENAME,
            expected_aal,
            expected_amr,
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "endpoint_url,is_r4",
        [
            ("", False),
            ("/FHIR/STU3/", False),
            ("/FHIR/R4/", True),
        ],
    )
    async def test_headers_on_echo_target_insufficient_ial(
        self,
        authenticate_user,
        service_url,
        referring_clinician_insufficient_ial,
        endpoint_url,
        is_r4,
    ):
        access_code = await authenticate_user(referring_clinician_insufficient_ial)

        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            _HEADER_REQUEST_ID: "DUMMY-VALUE",
            RenamedHeader.REFERRAL_ID.original: _EXPECTED_REFERRAL_ID,
            RenamedHeader.CORRELATION_ID.original: _EXPECTED_CORRELATION_ID,
            RenamedHeader.BUSINESS_FUNCTION.original: referring_clinician_insufficient_ial.business_function,
            RenamedHeader.ODS_CODE.original: referring_clinician_insufficient_ial.org_code,
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
            response.status_code == 401
        ), "Expected a 401 when accessing the api but got " + str(response.status_code)

        # Verify the response headers
        client_response_headers = response.headers
        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == _EXPECTED_CORRELATION_ID
        )
        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers

        # Verify the OperationOutcome payload
        response_data = response.json()
        assert response_data["resourceType"] == "OperationOutcome"
        assert response_data["meta"]["lastUpdated"] is not None
        assert len(response_data["meta"]["profile"]) == 1
        assert response_data["meta"]["profile"][0] == (
            "https://www.hl7.org/fhir/R4/operationoutcome.html"
            if is_r4
            else "https://fhir.nhs.uk/STU3/StructureDefinition/eRS-OperationOutcome-1"
        )
        assert len(response_data["issue"]) == 1
        issue = response_data["issue"][0]
        assert issue["severity"] == "error"
        assert issue["code"] == "forbidden"
        assert issue["diagnostics"] == (
            "We couldn't verify your identity. Contact your local Registration Authority "
            "or IT department for help."
        )
        assert len(issue["details"]["coding"]) == 1
        issue_details = issue["details"]["coding"][0]
        assert (
            issue_details["system"]
            == "https://fhir.nhs.uk/CodeSystem/NHSD-API-ErrorOrWarningCode"
            if is_r4
            else "https://fhir.nhs.uk/STU3/CodeSystem/eRS-APIErrorCode-1"
        )
        assert issue_details["code"] == "ACCESS_DENIED" if is_r4 else "NO_ACCESS"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "endpoint_url,is_fhir_4",
        [("", False), ("/FHIR/R4/", True), ("/FHIR/STU3/", False)],
    )
    async def test_headers_on_echo_target_insufficient_aal(
        self,
        authenticate_user,
        endpoint_url,
        is_fhir_4,
        service_url,
        update_user_restricted_product,
    ):
        # Add the AAL1 scope to our product so we can authenticate with AAL1 access for testing purposes.
        with update_user_restricted_product(
            append_scopes=["urn:nhsd:apim:user-nhs-id:aal1:e-referrals-service-api"]
        ):
            user: Actor = Actor.AAL1_USER
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
                response.status_code == 401
            ), "Expected a 401 when accessing the api but got " + str(
                response.status_code
            )

            assert response.reason == "Unauthorized"

            # Verify the response headers
            client_response_headers = response.headers
            assert (
                client_response_headers[RenamedHeader.CORRELATION_ID.original]
                == _EXPECTED_CORRELATION_ID
            )
            for renamed_header in RenamedHeader:
                assert renamed_header.renamed not in client_response_headers

            # Verify the OperationOutcome payload
            response_data = response.json()

            print(f"response_data={response_data}")

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
            assert issue["code"] == "login"
            assert issue["diagnostics"] == (
                "The authentication method utilised is not currently supported. Contact your local Registration Authority or IT department for help."
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
                issue_details["code"] == "ACCESS_DENIED" if is_fhir_4 else "NO_ACCESS"
            )

    @pytest.mark.asyncio
    async def test_headers_containing_comma_on_echo_target(
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
            RenamedHeader.FILENAME.original: _EXPECTED_COMMA_FILENAME,
            RenamedHeader.COMM_RULE_ORG.original: _EXPECTED_COMM_RULE_ORG,
            RenamedHeader.OBO_USER_ID.original: _EXPECTED_OBO_USER_ID,
        }

        # Make the API call
        response = requests.get(service_url, headers=client_request_headers)
        self.assert_ok_echo_response(
            response,
            service_url,
            referring_clinician,
            asid,
            _EXPECTED_COMMA_FILENAME,
            "3",
            "[N3_SMARTCARD]",
        )

    def assert_ok_echo_response(
        self,
        response: Response,
        service_url,
        referring_clinician,
        asid,
        expected_filename,
        expected_aal_value: str,
        expected_amr_value: str,
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
            target_request_headers[RenamedHeader.FILENAME.renamed] == expected_filename
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
        assert target_request_headers[_HEADER_AAL] == expected_aal_value
        assert target_request_headers[_HEADER_AMR] == expected_amr_value
        assert (
            target_request_headers[_HEADER_ID_ASSURANCE_LEVEL]
            == referring_clinician.id_assurance_level
        )

    @pytest.mark.asyncio
    async def test_access_mode_header_overwritten_on_echo_target(
        self, authenticate_user, service_url, referring_clinician, asid
    ):
        access_code = await authenticate_user(referring_clinician)

        client_request_headers = {
            _HEADER_ECHO: "",  # enable echo target
            _HEADER_AUTHORIZATION: "Bearer " + access_code,
            _HEADER_REQUEST_ID: "DUMMY-VALUE",
            _HEADER_ACCESS_MODE: "unknown-access-mode",
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
        self.assert_ok_echo_response(
            response,
            service_url,
            referring_clinician,
            asid,
            _EXPECTED_FILENAME,
            "3",
            "[N3_SMARTCARD]",
        )

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
        ), "Expected a 401 when accessing the api but got " + (str)(
            response.status_code
        )

        if not is_operation_outcome:
            assert len(response.content) == 0
        else:
            response_data = response.json()
            assert response_data["resourceType"] == "OperationOutcome"
            assert response_data["meta"]["lastUpdated"] is not None
            assert (
                response_data["meta"]["profile"][0]
                == "https://www.hl7.org/fhir/R4/operationoutcome.html"
            )
            assert len(response_data["issue"]) == 1
            issue = response_data["issue"][0]
            assert issue["severity"] == "error"
            assert issue["code"] == "login"
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
        ), "Expected a 401 when accessing the api but got " + (str)(
            response.status_code
        )

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
