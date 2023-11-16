from abc import abstractmethod
from functools import reduce
from typing import Callable, Dict, Iterable
from requests import Response
from pytest_check import check

import pytest
import asserts

from data import Actor, RenamedHeader
from utils import HttpMethod


@pytest.mark.sandbox
class SandboxTest:
    @pytest.fixture
    @abstractmethod
    def endpoint_url(self) -> str:
        pass

    @pytest.fixture
    @abstractmethod
    def http_method(self) -> HttpMethod:
        pass

    @pytest.fixture
    @abstractmethod
    def authorised_actors(self) -> Iterable[Actor]:
        pass

    @pytest.fixture
    def unauthorised_actors(
        self, authorised_actors: Iterable[Actor]
    ) -> Iterable[Actor]:
        return filter(lambda x: not (x in authorised_actors), Actor)

    @pytest.fixture
    @abstractmethod
    def default_headers(self) -> Dict[str, str]:
        return {}

    @pytest.fixture
    @abstractmethod
    def call_endpoint(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
    ) -> Callable[[Actor], Response]:
        pass

    @pytest.fixture
    @abstractmethod
    def allowed_business_functions(self) -> Iterable[str]:
        pass

    def test_unauthorised_business_functions(
        self,
        call_endpoint: Callable[[Actor], Response],
        allowed_business_functions: Iterable[str],
        unauthorised_actors: Iterable[Actor],
        http_method: HttpMethod,
        default_headers: Dict[str, str],
    ):
        for actor in unauthorised_actors:
            response = call_endpoint(actor, default_headers)

            asserts.assert_status_code(403, response.status_code)

            with check:
                authorised_business_function_str = reduce(
                    lambda x, y: x + "," + y, allowed_business_functions
                )
                expected_response = f"SANDBOX_ERROR: This endpoint cannot be accessed using the e-RS Business Function provided. Allowed values: {authorised_business_function_str}".encode()
                if http_method == HttpMethod.HEAD:
                    expected_response = "".encode()
                actual_response = response.content
                assert expected_response == actual_response, (
                    "\nUNEXPECTED RESPONSE: \n"
                    f"Actual response body = {actual_response}\n"
                    f"Expected response body = {expected_response}"
                )

    def test_with_correlation_id(
        self,
        call_endpoint: Callable[[Actor], Response],
        authorised_actors: Iterable[Actor],
        default_headers: Dict[str, str],
    ):
        assert (
            len(authorised_actors) > 0
        ), f"Current class {self.__class__.__name__} does not have any authorised users associated"

        correlation_id = "test"
        default_headers.update({RenamedHeader.CORRELATION_ID.original: correlation_id})

        response = call_endpoint(
            authorised_actors[0],
            headers=default_headers,
        )

        # Check that the response completed successfully.
        assert (
            response.status_code // 200 == 1
        ), "Supplied request did not complete successfully."

        with check:
            assert (
                response.headers[RenamedHeader.CORRELATION_ID.original]
                == correlation_id
            ), (
                "\nUNEXPECTED CORRELATION ID: \n"
                f"Actual Correlation ID = {response.headers[RenamedHeader.CORRELATION_ID.original]}\n"
                f"Expected Correlation ID = {correlation_id}"
            )

    @pytest.fixture
    def call_endpoint_url_with_request(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
        http_method: HttpMethod,
    ) -> Callable[[Actor, str, Dict[str, str]], Response]:
        return lambda actor, requestJson, headers={}: send_rest_request(
            http_method,
            endpoint_url,
            actor,
            json=load_json(requestJson),
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint_url_with_pathParam_and_request(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
        http_method: HttpMethod,
    ) -> Callable[[Actor, str, Dict[str, str], Dict[str, str]], Response]:
        return lambda actor, requestJson, params, headers={}: send_rest_request(
            http_method,
            endpoint_url.format(**params),
            actor,
            json=load_json(requestJson),
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint_url_with_pathParams(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        endpoint_url: str,
        http_method: HttpMethod,
    ) -> Callable[[Actor, Dict[str, str], Dict[str, str]], Response]:
        return lambda actor, params, headers={}: send_rest_request(
            http_method,
            endpoint_url.format(**params),
            actor,
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint_url_with_query(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
        http_method: HttpMethod,
    ) -> Callable[[Actor, Dict[str, str]], Response]:
        return lambda actor, queryParams={}, headers={}: send_rest_request(
            http_method,
            endpoint_url,
            actor,
            headers=headers,
            params=queryParams,
        )
