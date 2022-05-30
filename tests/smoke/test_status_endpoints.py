import pytest
from pytest_check import check
import requests
from jsonpath_rw import parse


@pytest.mark.smoke_test
class TestStatusEndpoints:
    def test_ping_endpoint(self, service_url):
        response = requests.get(f"{service_url}/_ping")
        with check:
            assert response.status_code == 200, (
                f"UNEXPECTED RESPONSE: "
                f"Actual response status code = {response.status_code}"
            )

    def test_status_endpoint(self, service_url, status_endpoint_api_key):
        response = requests.get(
            f"{service_url}/_status", headers={"apikey": status_endpoint_api_key}
        )
        with check:
            assert response.status_code == 200, (
                f"UNEXPECTED RESPONSE: "
                f"Actual response status code = {response.status_code}"
            )
        with check:
            expression = parse("$.status")
            matches = [match.value for match in expression.find(response.json())]
            assert matches.count("pass") == 1, (
                f"ACTUAL RESPONSE: = {response.json()}"
                f"UNEXPECTED RESPONSE: "
                f"Health check failed: $.status != 'pass'"
            )
        with check:
            expression = parse('$.checks["healthcheckService:status"][*].status')
            matches = [match.value for match in expression.find(response.json())]
            assert matches.count("pass") == len(matches), (
                f"UNEXPECTED RESPONSE: = {response.json()}"
                f"Health check failed: $.checks['healthcheckService:status'][*].status)] != 'pass'"
            )
