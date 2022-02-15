from enum import Enum


class Actor(Enum):
    # User ID, org code, business function
    RC = ("555031999105", "D82106", "REFERRING_CLINICIAN")
    RCA = ("555031998104", "D82106", "REFERRING_CLINICIAN_ADMIN")
    SPC = ("555032006106", "RCD", "SERVICE_PROVIDER_CLINICIAN")

    @property
    def user_id(self):
        return self.value[0]

    @property
    def org_code(self):
        return self.value[1]

    @property
    def business_function(self):
        return self.value[2]
