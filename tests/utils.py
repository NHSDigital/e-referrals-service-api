import pytest

from functools import wraps

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


def user_restricated_access(user: Actor):
    """
    Decorator indicating that a given function should be authenticated with User Restricted access with a supplied user.
    This will lead to a fixture named 'nhsd_apim_auth_headers' being provided to the function as a dictionary, including the headers required to authenticate as the supplied user.

    :param User: An Actor indicating the user to authenticate as. If no user is provided _DEFAULT_USER will be used instead.
    """

    _user: Actor = user if user else _DEFAULT_USER

    def decorator(func):
        @pytest.mark.nhsd_apim_authorization(
            {
                "access": "healthcare_worker",
                "level": "3",
                "login_form": {"username": _user.user_id},
            }
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(args, kwargs)

        return wrapper

    return decorator
