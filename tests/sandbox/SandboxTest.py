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
    def unauthorised_actors(self) -> Iterable[Actor]:
        pass

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
        unauthorised_actors: Iterable[Actor],
    ):
        authorised_actors = list(
            filter(lambda x: not (x in unauthorised_actors), Actor)
        )

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
