from enum import Enum
from typing import Iterable


class UserAuthenticationLevel(Enum):
    """
    Enum capturing the different supported authentication assurance levels supported for user-restricted access.
    """

    AAL3 = "aal3"
    AAL2 = "aal2"
    AAL1 = "aal1"


class Actor(Enum):
    # User ID, org code, business function, IAL, AAL, OBO User ID (optional)
    RC = (
        "555032000100",
        "D82106",
        "REFERRING_CLINICIAN",
        "3",
        UserAuthenticationLevel.AAL3,
    )
    RCA = (
        "555031998104",
        "D82106",
        "REFERRING_CLINICIAN_ADMIN",
        "3",
        UserAuthenticationLevel.AAL3,
    )
    RA = (
        "555031998103",
        "D82106",
        "REFERRING_ADMIN",
        "3",
        UserAuthenticationLevel.AAL3,
    )
    SPC = (
        "555032006106",
        "RCD",
        "SERVICE_PROVIDER_CLINICIAN",
        "3",
        UserAuthenticationLevel.AAL3,
    )
    SPA = (
        "555032006103",
        "RCD",
        "SERVICE_PROVIDER_ADMIN",
        "3",
        UserAuthenticationLevel.AAL3,
    )
    SPCA = (
        "555031998104",
        "RCD",
        "SERVICE_PROVIDER_CLINICIAN_ADMIN",
        "3",
        UserAuthenticationLevel.AAL3,
        "555031999105",
    )
    RC_DEV = (
        "021600556514",
        "R69",
        "REFERRING_CLINICIAN",
        "3",
        UserAuthenticationLevel.AAL3,
    )
    RC_INSUFFICIENT_IAL = (
        "555031999105",
        "D82106",
        "REFERRING_CLINICIAN",
        "2",
        UserAuthenticationLevel.AAL3,
    )
    AAL2_USER = (
        "656005750109",
        "RCD",
        "REFERRING_CLINICIAN",
        "3",
        UserAuthenticationLevel.AAL2,
    )
    AAL1_USER = (
        "656005750110",
        "RCD",
        "REFERRING_CLINICIAN",
        "3",
        UserAuthenticationLevel.AAL1,
    )

    @property
    def user_id(self):
        return self.value[0]

    @property
    def org_code(self):
        return self.value[1]

    @property
    def business_function(self):
        return self.value[2]

    @property
    def id_assurance_level(self):
        return self.value[3]

    @property
    def authentication_assurance_level(self) -> UserAuthenticationLevel:
        return self.value[4]

    @property
    def obo_user_id(self):
        if len(self.value) < 6:
            return None
        return self.value[5]

    def is_referrer(self):
        return self.business_function in [
            "REFERRING_CLINICIAN",
            "REFERRING_CLINICIAN_ADMIN",
            "REFERRING_ADMIN",
        ]

    @classmethod
    def all(
        cls,
        required_business_functions: Iterable[str] = [
            "REFERRING_CLINICIAN",
            "REFERRING_CLINICIAN_ADMIN",
            "REFERRING_ADMIN",
            "SERVICE_PROVIDER_CLINICIAN",
            "SERVICE_PROVIDER_CLINICIAN_ADMIN",
            "SERVICE_PROVIDER_ADMIN",
        ],
    ) -> Iterable["Actor"]:
        """
        Utility function for retrieving all Actor instances.

        :param required_business_functions: detail that only Actor instances with one of the provided business functions should be included.
        Defaults to all business functions (meaning that all Actor instances are returned).
        """
        return [
            actor
            for actor in cls
            if actor.business_function in required_business_functions
        ]


class RenamedHeader(Enum):
    CORRELATION_ID = ("x-correlation-id", "nhsd-correlation-id")
    BUSINESS_FUNCTION = ("nhsd-ers-business-function", "x-ers-business-function")
    ODS_CODE = ("NHSD-End-User-Organisation-ODS", "x-ers-ods-code")
    FILENAME = ("nhsd-ers-file-name", "x-ers-xapi-meta-file_name")
    COMM_RULE_ORG = ("nhsd-ers-comm-rule-org", "x-ers-xapi-comm-rule-org")
    REFERRAL_ID = ("nhsd-ers-referral-id", "x-ers-xapi-meta-intended_ubrn")
    OBO_USER_ID = ("nhsd-ers-on-behalf-of-user-id", "x-ers-obo-user-id")

    @property
    def original(self):
        return self.value[0]

    @property
    def renamed(self):
        return self.value[1]
