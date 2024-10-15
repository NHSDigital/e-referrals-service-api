import json
from typing import Dict, Iterable
from pytest_check import check
from requests import Response
from .data import RenamedHeader

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
}

_generic_file_headers = {
    "content-type": "application/pdf",
    "x-request-id": "58621d65-d5ad-4c3a-959f-0438e355990e-1",
    "vary": "origin",
    "cache-control": "no-cache",
    "accept-ranges": "bytes",
    "connection": "keep-alive",
    "access-control-expose-headers": "x-correlation-id,x-request-id,content-type,Location,ETag,Content-Disposition,Content-Length,Cache-Control",
}

_generic_upload_headers = {
    "content-type": "text/html; charset=utf-8",
    "x-request-id": "58621d65-d5ad-4c3a-959f-0438e355990e-1",
    "vary": "origin",
    "cache-control": "no-cache",
    "connection": "keep-alive",
    "content-length": "0",
    "access-control-expose-headers": "x-correlation-id,x-request-id,content-type,Location,ETag,Content-Disposition,Content-Length,Cache-Control",
}

# Headers which should be ignored from validation. This should only be used when the value of a header cannot be accurately be predicted.
# Note however the existance of these headers is still validated.
_ignored_headers = ["Date", "last-modified"]

# Headers which should be excluded from validation entirely.
_excluded_headers = ["Keep-Alive", "Strict-Transport-Security"]

_HEADER_REQUEST_ID = "x-request-id"
_HEADER_ERS_TRANSACTION_ID = "X_ERS_TRANSACTION_ID"


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


def assert_file_response(expected: bytes, actual: Response):
    """Assert that a supplied response is as expected"""
    with check:
        assert expected == actual.content, "\n UNEXPECTED RESPONSE: contents differ"


def assert_json_response_headers(response: Response, additional: Dict[str, str] = {}):
    assert_headers(response, _generic_headers, additional)


def assert_file_response_headers(response: Response, additional: Dict[str, str] = {}):
    assert_headers(response, _generic_file_headers, additional)


def assert_headers(
    response: Response,
    generic_headers: Dict[str, str],
    additional: Dict[str, str] = {},
    excluded: Iterable[str] = [],
):
    """
    Assert that a supplied response containes the expected headers, ignoring casing for header names.

    :param additional any additional headers that should be included

    """

    actual_headers = _lower_keys(
        dict(
            filter(
                _filter_header,
                response.headers.items(),
            )
        )
    )

    expected_headers = dict(generic_headers)
    expected_headers.update(additional)
    expected_headers = _lower_keys(expected_headers)

    # Content is uncompressed for < 1MB see sandbox/node_modules/@hapi/hapi/lib/compression.js

    if "content-length" in response.headers:
        content_length_header = int(response.headers["content-length"])

        if (content_length_header is not None) and (content_length_header < 1024):
            expected_headers.update({"vary": "origin"})
            expected_headers.update({"content-length": str(content_length_header)})
            try:
                del (
                    expected_headers["transfer-encoding"],
                    expected_headers["content-encoding"],
                )
            except KeyError:
                pass

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


def assert_upload_response_headers(
    response: Response, additional: Dict[str, str] = {}, excluded: Iterable[str] = []
):
    """
    Assert that a supplied response containes the expected headers, ignoring casing for header names.

    :param additional any additional headers that should be included

    """

    actual_headers = _lower_keys(
        dict(
            filter(
                _filter_header,
                response.headers.items(),
            )
        )
    )

    expected_headers = dict(_generic_upload_headers)
    expected_headers.update(additional)
    expected_headers = _lower_keys(expected_headers)

    with check:
        assert expected_headers == actual_headers, (
            "\n UNEXPECTED HEADERS: \n"
            f"Expected Headers = {expected_headers}\n"
            f"Actual Headers = {actual_headers}\n"
            f"Differences = {expected_headers.items() ^ actual_headers.items()}"
        )


def _filter_header(header: str) -> bool:
    ignored_headers = _ignored_headers + _excluded_headers
    return not (header[0] in ignored_headers)


def _lower_keys(dict: Dict[str, str]) -> Dict[str, str]:
    return {key.lower(): value for key, value in dict.items()}


def assert_ok_response(response: Response, expected_correlation_id: int):
    # Verify the status
    assert (
        response.status_code == 200
    ), "Expected a 200 when accessing the api but got " + (str)(response.status_code)

    # Verify the response headers
    client_response_headers = response.headers
    assert (
        client_response_headers[RenamedHeader.CORRELATION_ID.original]
        == expected_correlation_id
    )
    assert len(client_response_headers[_HEADER_REQUEST_ID]) > 10
    assert _HEADER_ERS_TRANSACTION_ID not in client_response_headers

    for renamed_header in RenamedHeader:
        assert renamed_header.renamed not in client_response_headers


def assert_error_response(
    response: Response, expected_correlation_id: int, expected_status_code: int
):
    # Verify the status
    assert response.status_code == expected_status_code, (
        "Expected a "
        + expected_status_code
        + " when accessing the api but got "
        + (str)(response.status_code)
    )

    assert len(response.content) == 0

    # Verify the response headers
    client_response_headers = response.headers

    assert (
        client_response_headers[RenamedHeader.CORRELATION_ID.original]
        == expected_correlation_id
    )

    for renamed_header in RenamedHeader:
        assert renamed_header.renamed not in client_response_headers


def assert_error_response_with_body(
    response: Response, expected_correlation_id: int, expected_status_code: int
):
    # Verify the status
    assert response.status_code == expected_status_code, (
        "Expected a "
        + expected_status_code
        + " when accessing the api but got "
        + (str)(response.status_code)
    )

    assert len(response.content) > 0

    # Verify the response headers
    client_response_headers = response.headers

    assert (
        client_response_headers[RenamedHeader.CORRELATION_ID.original]
        == expected_correlation_id
    )

    for renamed_header in RenamedHeader:
        assert renamed_header.renamed not in client_response_headers
