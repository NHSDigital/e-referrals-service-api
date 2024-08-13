import pytest

from functools import wraps
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


def user_restricated_access(user: Actor = None):
    """
    Decorator indicating that a given function should be authenticated with User Restricted access with a supplied user.
    This will lead to a fixture named 'nhsd_apim_auth_headers' being provided to the function as a dictionary, including the headers required to authenticate as the supplied user.

    :param User: An Actor indicating the user to authenticate as. If no user is provided _DEFAULT_USER will be used instead.
    """

    # Need to check that the provided user both exists and is of type Actor as non-parameterised decorators in python are pass with the wrapped
    # function as their first argument.
    _user: Actor = user if type(user) == Actor else _DEFAULT_USER

    def decorator(func):
        # if the decorated function is async, return an async function.
        if iscoroutinefunction(func):

            @pytest.mark.nhsd_apim_authorization(
                {
                    "access": "healthcare_worker",
                    "level": "3",
                    "login_form": {"username": _user.user_id},
                }
            )
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)

        else:

            @pytest.mark.nhsd_apim_authorization(
                {
                    "access": "healthcare_worker",
                    "level": "3",
                    "login_form": {"username": _user.user_id},
                }
            )
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

        # use functools.wraps to maintain the function details of the decorated function on the result.
        return wraps(func)(wrapper)

    return decorator
