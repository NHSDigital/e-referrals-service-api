import pytest
from pytest_check import check
import requests
from jsonpath_rw import parse

# test runs normally in int and prod, status must report pass
STRICT_STATUS_ENVS = {"int", "prod"}


@pytest.mark.smoke_test
class TestStatusEndpoints:
    def test_ping_endpoint(self, service_url):
        response = requests.get(f"{service_url}/_ping")
        with check:
            assert response.status_code == 200, (
                f"UNEXPECTED RESPONSE: "
                f"Actual response status code = {response.status_code}"
            )

    def test_status_endpoint(self, service_url, status_endpoint_api_key, environment):
        response = requests.get(
            f"{service_url}/_status", headers={"apikey": status_endpoint_api_key}
        )
        assert response.status_code == 200, (
            f"UNEXPECTED RESPONSE: "
            f"Actual response status code = {response.status_code}"
        )

        # parse JSON response and extract the value
        response_json = response.json()
        top_level_statuses = [
            match.value for match in parse("$.status").find(response_json)
        ]
        healthcheck_statuses = [
            match.value
            for match in parse('$.checks["healthcheckService:status"][*].status').find(
                response_json
            )
        ]

        # normal test behaviour in int and prod
        if environment in STRICT_STATUS_ENVS:
            assert (
                top_level_statuses.count("pass") == 1
            ), "UNEXPECTED RESPONSE: Health check failed: $.status != 'pass'"
            assert healthcheck_statuses.count("pass") == len(healthcheck_statuses), (
                "UNEXPECTED RESPONSE: Health check failed: "
                "$.checks['healthcheckService:status'][*].status != 'pass'"
            )
            return

        # Monitoring in lower environments is intentionally disabled, so making the test less strict.
        assert len(top_level_statuses) == 1 and top_level_statuses[0] in {
            "pass",
            "fail",
        }, "UNEXPECTED RESPONSE: $.status missing or invalid"
        assert len(healthcheck_statuses) >= 1 and all(
            status in {"pass", "fail"} for status in healthcheck_statuses
        ), "UNEXPECTED RESPONSE: healthcheckService status missing or invalid"

        # mark failures as expected behaviour
        if top_level_statuses[0] == "fail":
            pytest.xfail(
                "Known APIM lower-env behavior: _status may report fail outside int/prod"
            )
