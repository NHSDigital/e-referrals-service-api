import pytest

import state

from functools import wraps
from typing import Callable, List
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

    :param user: An Actor indicating the user to authenticate as. If no user is provided _DEFAULT_USER will be used instead.
    """

    def decorator(func):
        auth_args = {
            "access": "healthcare_worker",
            "level": "aal3",
            "login_form": {"username": user.user_id},
        }

        @pytest.mark.nhsd_apim_authorization(auth_args)
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with state.authentication_context(
                state.AuthenticationConfig.user_restricted_config()
            ):
                return await func(*args, **kwargs)

        @pytest.mark.nhsd_apim_authorization(auth_args)
        @wraps(func)
        def wrapper(*args, **kwargs):
            with state.authentication_context(
                state.AuthenticationConfig.user_restricted_config()
            ):
                return func(*args, **kwargs)

        # if the decorated function is async, return an async function, else return a synchronous version.
        return async_wrapper if iscoroutinefunction(func) else wrapper

    # If a function is provided the decorator is being called without any parameters and we need to call our decorator supplying this as the function.
    # Otherwise the decorator is being called with arguments and can be returned directly.
    return decorator(function) if function else decorator


def app_restricted_access(types: List[state.ApplicationRestrictedType]):
    """
    Decorator indicating that the given function should be authenticated with Application Restricted access with a list of set types.
    This will lead to a fixture named 'nhsd_apim_auth_headers' being provided to the function as a dictionary, including the headers required to authenticate as the default application.

    :param types: A list of ApplicationRestrictedType values indicating the types of application restricted access the decorated function should be authenticated with.
    """

    def decorator(func):
        auth_args = {"access": "application", "level": "level3"}

        @pytest.mark.nhsd_apim_authorization(auth_args)
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            for type in types:
                with state.authentication_context(
                    state.AuthenticationConfig.application_restricted_config(type=type)
                ):
                    return await func(*args, **kwargs)

        @pytest.mark.nhsd_apim_authorization(auth_args)
        @wraps(func)
        def wrapper(*args, **kwargs):
            for type in types:
                with state.authentication_context(
                    state.AuthenticationConfig.application_restricted_config(type=type)
                ):
                    return func(*args, **kwargs)

        # if the decorated function is async, return an async function as a decorator, otherwise use a synchronous decorator.
        return async_wrapper if iscoroutinefunction(func) else wrapper

    return decorator
