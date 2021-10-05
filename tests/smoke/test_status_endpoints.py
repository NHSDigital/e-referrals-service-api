import pytest
from pytest_check import check
import requests
from configuration import config
from jsonpath_rw import parse

@pytest.mark.smoke_test
class TestStatusEndpoints:

    def test_ping_endpoint(self):
        response = requests.get(
            f"{config.BASE_URL}/{config.ERS_BASE_PATH}/_ping"
        )
        with check:
            assert response.status_code == 200, (
                f"UNEXPECTED RESPONSE: "
                f"Actual response status code = {response.status_code}"
            )
            
    def test_status_endpoint(self):
        response = requests.get(
            f"{config.BASE_URL}/{config.ERS_BASE_PATH}/_status",
            headers = {"apikey": config.STATUS_ENDPOINT_API_KEY}
        )
        with check:
            assert response.status_code == 200, (
                f"UNEXPECTED RESPONSE: "
                f"Actual response status code = {response.status_code}"
            )
        with check:
            expression = parse('$.status')
            matches = [match.value for match in expression.find(response.json())]
            assert matches.count('pass') == 1, (
                f"UNEXPECTED RESPONSE: "
                f"Health check failed: $.status != 'pass'"
            )
        with check:
            expression = parse('$.checks["healthcheckService:status"][*].status')
            matches = [match.value for match in expression.find(response.json())]
            assert matches.count('pass') == len(matches), (
                f"UNEXPECTED RESPONSE: "
                f"Health check failed: $.checks['healthcheckService:status'][*].status)] != 'pass'"
            )
