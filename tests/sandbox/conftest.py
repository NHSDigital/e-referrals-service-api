import os

import pytest
import json
import requests

from typing import Dict, Callable

from data import Actor, RenamedHeader
from utils import HttpMethod


@pytest.fixture(scope="session")
def sandbox_url(environment, service_url) -> str:
    """Provides an overload for the standard service_url fixture to support running the sandbox against a local deployment"""
    return "http://127.0.0.1:9100" if environment == "local" else service_url


@pytest.fixture(scope="session")
def load_json(environment) -> Callable[[str], Dict[str, str]]:
    """Provides a method which encapsulates the logic of retrieving some example JSON from a file"""
    base_path = (
        "sandbox"
        if environment == "local"
        else "proxies/sandbox/apiproxy/resources/hosted"
    )
    return lambda path: _get_json(base_path + "/src/mocks/", path)


@pytest.fixture(scope="session")
def load_file(environment) -> Callable[[str], bytes]:
    """Provides a method which encapsulates the logic of retrieving some example JSON from a file"""
    base_path = (
        "sandbox"
        if environment == "local"
        else "proxies/sandbox/apiproxy/resources/hosted"
    )
    return lambda path: _get_file(base_path + "/src/mocks/", path)


@pytest.fixture
def send_rest_request(
    sandbox_url,
) -> Callable[[HttpMethod, str, Actor], requests.Response]:
    """Provides a method which encapsulates the logic of sending a REST call to the correct base URL"""
    return lambda method, url, actor, headers={}, **kwargs: _send_rest_request(
        method, sandbox_url + "/" + url, actor, headers, **kwargs
    )


def _get_json(base_path: str, path: str) -> Dict[str, str]:
    with open(base_path + path) as f:
        return json.load(f)


def _get_file(base_path: str, path: str) -> bytes:
    with open(base_path + path, "rb") as f:
        return f.read(-1)


def _send_rest_request(
    method: HttpMethod, url: str, actor: Actor, headers: Dict[str, str], **kwargs
) -> requests.Response:
    headers[RenamedHeader.BUSINESS_FUNCTION.original] = actor.business_function
    if actor.obo_user_id != None:
        headers[RenamedHeader.OBO_USER_ID.original] = actor.obo_user_id
    return method(url, headers=headers, **kwargs)
