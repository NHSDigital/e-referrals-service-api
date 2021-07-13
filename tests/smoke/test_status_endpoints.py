import pytest
from pytest_check import check
import requests
from configuration import config

@pytest.mark.smoke_test
class TestStatusEndpoints:

    def test_ping_endpoint(self):
        response = requests.get(
            f"{config.BASE_URL}/{config.ERS_BASE_PATH}/_ping"
        )
        with check:
            assert response.status_code == 200, (
                f"UNEXPECTED RESPONSE:"
                f"actual response status id { response.status_code}"
            )
            