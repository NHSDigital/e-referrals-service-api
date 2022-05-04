import pytest
import requests
from data import Actor, RenamedHeader

HEADER_AUTHORIZATION = "Authorization"
HEADER_REQUEST_ID = "x-request-id"

EXPECTED_CORRELATION_ID = "123123-123123-123123-123123"
EXPECTED_ACTOR = Actor.AA

SPECIALTY_REF_DATA_URL = "/FHIR/STU3/CodeSystem/SPECIALTY"


@pytest.mark.integration_test
class TestAppRestricted:
    @pytest.mark.parametrize("actor", [(EXPECTED_ACTOR)])
    def test_authorised_application_not_supported(
        self, access_code, service_url, actor
    ):
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
            response.status_code == 403
        ), "Expected a 403 when accesing the api but got " + (str)(response.status_code)

        assert len(response.content) == 0

        # Verify the response headers
        client_response_headers = response.headers

        assert (
            client_response_headers[RenamedHeader.CORRELATION_ID.original]
            == EXPECTED_CORRELATION_ID
        )

        for renamed_header in RenamedHeader:
            assert renamed_header.renamed not in client_response_headers
