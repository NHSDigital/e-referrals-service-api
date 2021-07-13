import pytest
from pytest_check import check
import requests

@pytest.mark.smoke_test
class TestStatusEndpoints:

    def test_ping_endpoint(self):
        response = requests.get(
            f"https://internal-dev.api.service.nhs.uk/referrals-alpha/_ping"
        )
        with check:
            assert response.status_code == 200, (
                f"UNEXPECTED RESPONSE:"
                f"actual response status id { response.status_code}"
            )
            