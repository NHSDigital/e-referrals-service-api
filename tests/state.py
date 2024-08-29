from typing import Dict
from enum import Enum
from contextlib import contextmanager

from utils import get_env


def _is_mocked_environment() -> bool:
    return get_env("ENVIRONMENT") == "internal-dev" and "ft" in get_env(
        "SERVICE_BASE_PATH"
    )


def _calculate_default_asid() -> str:
    return (
        get_env("ERS_MOCK_ASID")
        if _is_mocked_environment()
        else get_env("ERS_TEST_ASID")
    )


def _calculate_default_app_restricted_ods_code() -> str:
    return "R68" if _is_mocked_environment() else "RCD"


def _calculate_default_app_restricted_user_id() -> str:
    return "000000000101" if _is_mocked_environment() else "555032000100"


class ApplicationRestrictedType(Enum):
    REFERRER = "REFERRER_APPLICATION_RESTRICTED"
    PROVIDER = "PROVIDER_APPLICATION_RESTRICTED"


class AuthenticationConfig:
    """
    Defines some configuration for use as part of authentication.
    """

    def __init__(self, app_attributes: Dict[str, str]):
        self._app_attributes = app_attributes

    @property
    def app_attributes(self) -> Dict[str, str]:
        """
        Any attributes that should be included against the application used for authentication within Apigee.
        """

        # return a new dict to hide the internal parameters so they cannot be modified via the public interface.
        return dict(self._app_attributes)

    @staticmethod
    def user_restricted_config(
        asid: str = _calculate_default_asid(),
    ) -> "AuthenticationConfig":
        """
        Create a AuthenticationConfig object detaililng that authentication should be completed using User Restricted based authentication.

        :param asid: a string detailing the ASID value to be associated with the app used for authentication. Defaults to the result of _calculate_default_asid().
        :returns: a new AuthenticationConfig object configured for User Restricted access.
        """

        return AuthenticationConfig(app_attributes={"asid": asid})

    @staticmethod
    def application_restricted_config(
        type: ApplicationRestrictedType,
        user_id: str = _calculate_default_app_restricted_user_id(),
        ods_code: str = _calculate_default_app_restricted_ods_code(),
        asid: str = _calculate_default_asid(),
    ) -> "AuthenticationConfig":
        """
        Create a AuthenticationConfig object detailing that authentication should be completed using Application Restricted based authentication.

        :param type: a ApplicationRestrictedType detailing the type of Application Restricted access to be utilised.
        :param user_id: the user ID to be associated with the app used for authentication. Defaults to the result of _calculate_default_app_restricted_user_id().
        :param ods_code: the ODS code to be associated with the app used for authentication. Defaults to the result of _calculate_default_app_restricted_ods_code().
        :param asid: a string detailing the ASID value to be associated with the app used for authentication. Defaults to the result of _calculate_default_asid().

        :returns: a new AuthenticationConfig object configured for Application Restricted access.
        """

        if type not in ApplicationRestrictedType:
            raise ValueError(
                f"Provided type not supported. Supported_business_functions={list(ApplicationRestrictedType)} provided_type={type}"
            )

        return AuthenticationConfig(
            app_attributes={
                "asid": asid,
                "app-restricted-business-function": type.value,
                "app-restricted-ods-code": ods_code,
                "app-restricted-user-id": user_id,
            }
        )


_AUTHENTICATION_CONFIG_INSTANCE = None


@contextmanager
def authentication_context(config: AuthenticationConfig) -> AuthenticationConfig:
    """
    Stores the supplied AuthenticationConfig so it can be used by other fixtures/test utilities.
    Returns the provided AuthenticationConfig within a contextmanager which will handle the clear down of clearing the provided configuration.

    Standard usage:

    config = AuthenticationConfig.user_restricted_config()

    with authentication_context(config):
        # test logic....

    :param config: An AuthenticationConfig object detailing the configuration that should be stored for the current test context.
    :returns: the provided config wrapped as a contextmanager.
    """
    _AUTHENTICATION_CONFIG_INSTANCE = config
    try:
        yield _AUTHENTICATION_CONFIG_INSTANCE
    finally:
        _AUTHENTICATION_CONFIG_INSTANCE = None


def current_authentication_context() -> AuthenticationConfig:
    """
    Retrieve the AuthenticationConfig instance being used within the current test context.

    :returns: the current AuthenticationConfig
    :throws ValueError: if no AuthenticationConfig has been configured for the current test context.
    """
    if not _AUTHENTICATION_CONFIG_INSTANCE:
        raise ValueError(
            "No authentication configuration is currently instantiated. Has with_authentication_context been called?"
        )

    return _AUTHENTICATION_CONFIG_INSTANCE
