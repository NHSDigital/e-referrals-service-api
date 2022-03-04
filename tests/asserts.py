import json
from typing import Dict
from pytest_check import check
from requests import Response

# Headers which are expected for all requests
_generic_headers = {
    "content-type": "application/fhir+json",
    "x-request-id": "58621d65-d5ad-4c3a-959f-0438e355990e-1",
    "vary": "origin,accept-encoding",
    "cache-control": "no-cache",
    "accept-ranges": "bytes",
    "content-encoding": "gzip",
    "connection": "keep-alive",
    "transfer-encoding": "chunked",
    "access-control-expose-headers": "x-correlation-id,x-request-id,content-type,Location,ETag,Content-Disposition,Content-Length,Cache-Control",
    "strict-transport-security": "max-age=864000; includeSubDomains",
}

# Headers which should be ignored from validation. This should only be used when the value of a header cannot be accurately be predicted.
# Note however the existance of these headers is still validated.
_ignored_headers = ["Date", "last-modified"]

# Headers which should be excluded from validation entirely.
_excluded_headers = ["Keep-Alive"]


def assert_status_code(expected: int, actual: int):
    """Assert that supplied status code is as expected"""
    with check:
        assert expected == actual, (
            "\n UNEXPECTED RESPONSE: \n"
            f"Expected Status Code = {expected}\n"
            f"Actual Status Code = {actual}"
        )


def assert_response(expected: Dict[str, str], actual: Response):
    """Assert that a supplied response is as expected"""
    with check:
        actual_response = json.loads(actual.content)
        assert expected == actual_response, (
            "\n UNEXPECTED RESPONSE: \n"
            f"Expected Response = {expected}\n"
            f"Actual Response = {actual_response}"
        )


def assert_headers(response: Response, additional: Dict[str, str] = {}):
    """
    Assert that a supplied response containes the expected headers, ignoring casing for header names.

    :param additional any additional headers that should be included

    """
    expected_headers = dict(_generic_headers)
    expected_headers.update(additional)
    expected_headers = _lower_keys(expected_headers)

    actual_headers = _lower_keys(
        dict(filter(_filter_header, response.headers.items(),))
    )

    with check:
        assert expected_headers == actual_headers, (
            "\n UNEXPECTED HEADERS: \n"
            f"Expected Headers = {expected_headers}\n"
            f"Actual Headers = {actual_headers}\n"
            f"Differences = {expected_headers.items() ^ actual_headers.items()}"
        )

    with check:
        for header in _ignored_headers:
            assert header in response.headers, (
                "\n Expected header does not exist\n"
                f"Expected header = {header}\n"
                f"Actual headers = {[header[0] for header in response.headers.items()]}"
            )


def _filter_header(header: str) -> bool:
    ignored_headers = _ignored_headers + _excluded_headers
    return not (header[0] in ignored_headers)


def _lower_keys(dict: Dict[str, str]) -> Dict[str, str]:
    return {key.lower(): value for key, value in dict.items()}
