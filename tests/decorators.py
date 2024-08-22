import pytest

from functools import wraps
from typing import Callable
from asyncio import iscoroutinefunction

from data import Actor
from conftest import get_env


def _calculate_default_user() -> Actor:
    return (
        Actor.RC_DEV
        if get_env("ENVIRONMENT") == "internal-dev"
        and "ft" in get_env("SERVICE_BASE_PATH")
        else Actor.RC
    )


_DEFAULT_USER: Actor = _calculate_default_user()


def user_restricated_access(function: Callable = None, user: Actor = _DEFAULT_USER):
    """
    Decorator indicating that a given function should be authenticated with User Restricted access with a supplied user.
    This will lead to a fixture named 'nhsd_apim_auth_headers' being provided to the function as a dictionary, including the headers required to authenticate as the supplied user.

    :param User: An Actor indicating the user to authenticate as. If no user is provided _DEFAULT_USER will be used instead.
    """

    def decorator(func):
        kwargs = {
            "access": "healthcare_worker",
            "level": "3",
            "login_form": {"username": user.user_id},
        }

        @pytest.mark.nhsd_apim_authorization(kwargs)
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        @pytest.mark.nhsd_apim_authorization(kwargs)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # if the decorated function is async, return an async function, else return a synchronous version.
        return async_wrapper if iscoroutinefunction(func) else wrapper

    # If a function is provided the decorator is being called without any parameters and we need to call our decorator supplying this as the function.
    # Otherwise the decorator is being called with arguments and can be returned directly.
    return decorator(function) if function else decorator
