#!/usr/bin/env python3
"""
set_version.py

Reads an openapi spec on stdin and substitutes placeholders with values stored in dictionary,
then prints it on stdout.
"""
import sys


def main():
    """Main entrypoint"""
    substitutes_dict = {
        "[[HYPERLINK_A004]]": "[A004 - Retrieve reference data](#api-Default-a004-retrieve-reference-data)",
        "[[HYPERLINK_A005]]": "[A005 - Retrieve referral request](#api-Default-a005-retrieve-referral-request)",
        "[[HYPERLINK_A006]]": "[A006 - Retrieve attachment](#api-Default-a006-retrieve-attachment)",
        "[[HYPERLINK_A007]]": "[A007 - Retrieve clinical information](#api-Default-a007-retrieve-clinical-information)",
        "[[HYPERLINK_A008]]": "[A008 - Retrieve referral worklist](#api-Default-a008-retrieve-worklist)",
        "[[HYPERLINK_A010]]": "[A010 - Patient service search](#api-Default-a010-patient-service-search)",
        "[[HYPERLINK_A011]]": "[A011 - Create referral](#api-Default-a011-create-referral)",
        "[[HYPERLINK_A012]]": "[A012 - Maintain referral letter](#api-Default-a012-maintain-referral-letter)",
        "[[HYPERLINK_A013]]": "[A013 - Accept referral](#api-Default-a013-accept-referral)",
        "[[HYPERLINK_A014]]": "[A014 - Reject referral](#api-Default-a014-reject-referral)",
        "[[HYPERLINK_A015]]": "[A015 - Retrieve appointment slots](#api-Default-a015-retrieve-appointment-slots)",
        "[[HYPERLINK_A016]]": "[A016 - Book or defer appointment](#api-Default-a016-book-or-defer-appointment)",
        "[[HYPERLINK_A019]]": "[A019 - Generate patient letter](#api-Default-a019-generate-patient-letter)",
        "[[HYPERLINK_A020]]": "[A020 - Upload file to document store](#api-Default-a020-upload-file-to-document-store)",
        "[[HYPERLINK_A021]]": "[A021 - Create referral and send for triage](#api-Default-a021-create-referral-request-and-send-for-triage)",
        "[[HYPERLINK_A022]]": "[A022 - Cancel appointment, action later](#api-Default-a022-cancel-appointment-action-later)",
        "[[HYPERLINK_A023]]": "[A023 - Retrieve advice and guidance requests worklist](#api-Default-a023-retrieve-a&g-worklist)",
        "[[HYPERLINK_A024]]": "[A024 - Retrieve advice and guidance request summary](#api-Default-a024-retrieve-advice-and-guidance)",
        "[[HYPERLINK_A025]]": "[A025 - Retrieve advice and guidance conversation](#api-Default-a025-retrieve-advice-and-guidance-conversation)",
        "[[HYPERLINK_A026]]": "[A026 - Send advice and guidance response](#api-Default-a026-send-a&g-response)",
        "[[HYPERLINK_A027]]": "[A027 - Convert advice and guidance request to referral](#api-Default-a027-convert-a&g-to-referral)",
        "[[HYPERLINK_A028]]": "[A028 - Record triage outcome](#api-Default-a028-record-triage-outcome)",
        "[[HYPERLINK_A029]]": "[A029 - Available actions for user list](#api-Default-a029-available-actions-for-user-list)",
        "[[HYPERLINK_A030]]": "[A030 - Retrieve e-RS business functions](#api-Default-a030-retrieve-business-functions)",
        "[[HYPERLINK_A031]]": "[A031 - Change shortlist](#api-Default-a031-change-shortlist)",
        "[[HYPERLINK_A032]]": "[A032 - Change shortlist and send for triage](#api-Default-a032-change-shortlist-and-send-for-triage)",
        "[[HYPERLINK_A033]]": "[A033 - Retrieve healthcare service](#api-Default-a033-retrieve-healthcare-service)",
        "[[HYPERLINK_A034]]": "[A034 - Update appointment](#api-Default-a034-update-appointment)",
        "[[HYPERLINK_A035]]": "[A035 - Search for healthcare services](#api-Default-a035-search-for-healthcare-services)",
        "[[HYPERLINK_A036]]": "[A036 - Cancel referral](#api-Default-a036-cancel-referral)",
        "[[HYPERLINK_A037]]": "[A037 - Retrieve healthcare service version](#api-Default-a037-retrieve-healthcare-service-version)",
        "[[HYPERLINK_A038]]": "[A038 - Retrieve appointment](#api-Default-a038-retrieve-appointment)",
        "[[HYPERLINK_A039]]": "[A039 - Request pre-signed URL to upload file to document store](#api-Default-a039-request-url-large-file-upload)",
        "[[HYPERLINK_A040]]": "[A040 - Retrieve e-RS-Specific Practitioner Information](#api-Default-a040-retrieve-practitioner-info)",
        "[[HYPERLINK_A043]]": "[A043 - Retrieve advice and guidance overview PDF](#api-Default-a043-retrieve-advice-and-guidance-overview-pdf)",
        "[[HYPERLINK_ONBOARDING]]": "[onboarding](#api-description__onboarding)",
        "[[HYPERLINK_STABLE]]": "[stable](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#api-status)",
        "[[HYPERLINK_BETA]]": "[beta](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#api-status)",
        "[[HYPERLINK_PDS]]": "[Personal Demographic Service (PDS)](https://digital.nhs.uk/developer/api-catalogue/personal-demographics-service-fhir)",
        "[[HYPERLINK_CIS2]]": "[CIS2](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/user-restricted-restful-apis-nhs-cis2-combined-authentication-and-authorisation)",
        "[[HYPERLINK_ERS_BUS_FUNCTIONS]]": "[e-RS Business Functions](https://fhir.nhs.uk/CodeSystem/eRS-BusinessFunction-1)",
        "[[HYPERLINK_PERFORMANCE_TESTING]]": "[performance testing](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#performance-testing)",
        "[[HYPERLINK_CONTACT_US]]": "[contact us](https://digital.nhs.uk/developer/help-and-support)",
    }

    data = sys.stdin.read()

    for key, value in substitutes_dict.items():
        data = data.replace(key, value)

    sys.stdout.write(data)
    sys.stdout.close()


if __name__ == "__main__":
    main()
