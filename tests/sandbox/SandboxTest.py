from abc import abstractmethod
from functools import reduce
from typing import Callable, Dict, Iterable, NoReturn
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
    def endpoint_versioned_url(self) -> str:
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

    # @pytest.fixture
    # @abstractmethod
    # def unauthorised_actors(self) -> Iterable[Actor]:
    # pass

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
    ):
        for actor in unauthorised_actors:
            response = call_endpoint(actor)

            asserts.assert_status_code(403, response.status_code)

            with check:
                authorised_business_function_str = reduce(
                    lambda x, y: x + "," + y, allowed_business_functions
                )
                expected_response = f"SANDBOX_ERROR: This endpoint cannot be accessed using the e-RS Business Function provided. Allowed values: {authorised_business_function_str}".encode()
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
    ):
        assert (
            len(authorised_actors) > 0
        ), f"Current class {self.__class__.__name__} does not have any authorised users associated"

        correlation_id = "test"
        response = call_endpoint(
            authorised_actors[0],
            headers={RenamedHeader.CORRELATION_ID.original: correlation_id},
        )
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
    ) -> Callable[[Actor, str], Response]:
        return lambda actor, requestJson, headers={}: send_rest_request(
            HttpMethod.POST,
            endpoint_url,
            actor,
            json=load_json(requestJson),
            headers=headers,
        )

    @pytest.fixture
    def call_put_endpoint_url_with_request(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
    ) -> Callable[[Actor, str], Response]:
        return lambda actor, requestJson, headers={}: send_rest_request(
            HttpMethod.PUT,
            endpoint_url,
            actor,
            json=load_json(requestJson),
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint_url_with_value_and_version(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        endpoint_versioned_url: str,
    ) -> Callable[[Actor, str, str], Response]:
        return lambda actor, value, version, headers={}: send_rest_request(
            HttpMethod.GET,
            endpoint_versioned_url.format(param1=value, param2=version),
            actor,
            headers=headers,
        )

    @pytest.fixture
    def call_endpoint_url_with_value(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
    ) -> Callable[[Actor, str], Response]:
        return lambda actor, param, headers={}: send_rest_request(
            HttpMethod.GET, endpoint_url.format(param=param), actor, headers=headers,
        )

    @pytest.fixture
    def call_get_endpoint_url_with_query(
        self,
        send_rest_request: Callable[[HttpMethod, str, Actor], Response],
        load_json: Callable[[str], Dict[str, str]],
        endpoint_url: str,
    ) -> Callable[[Actor, Dict[str, str]], Response]:
        return lambda actor, queryParams, headers={}: send_rest_request(
            HttpMethod.GET, endpoint_url, actor, headers=headers, params=queryParams,
        )
