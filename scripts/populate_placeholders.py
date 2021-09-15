#!/usr/bin/env python3
"""
set_version.py

Reads an openapi spec on stdin and substitutes placeholders with values sotred in dictionary,
then prints it on stdout.
"""
import sys


def main():
    """Main entrypoint"""
    substitutes_dict = {
        "[[HYPERLINK_A005]]": "[A005 - Retrieve referral request](#api-Default-a005-retrieve-referral-request)",
        "[[HYPERLINK_A006]]": "[A006 - Retrieve attachment](#api-Default-a006-retrieve-attachment)",
        "[[HYPERLINK_A007]]": "[A007 - Retrieve clinical information](#api-Default-a007-retrieve-clinical-information)",
        "[[HYPERLINK_A010]]": "[A010 - Patient service search](#api-Default-a010-patient-service-search)",
        "[[HYPERLINK_A011]]": "[A011 - Create referral](#api-Default-a011-create-referral)",
        "[[HYPERLINK_A012]]": "[A012 - Maintain referral letter](#api-Default-a012-maintain-referral-letter)",
        "[[HYPERLINK_A015]]": "[A015 - Retrieve appointment slots](#api-Default-a015-retrieve-appointment-slots)",
        "[[HYPERLINK_A016]]": "[A016 - Book or defer appointment](#api-Default-a016-book-or-defer-appointment)",
        "[[HYPERLINK_A019]]": "[A019 - Generate patient letter](#api-Default-a019-generate-patient-letter)",
        "[[HYPERLINK_A020]]": "[A020 - Upload file to document store](#api-Default-a020-upload-file-to-document-store)",
        "[[HYPERLINK_A021]]": "[A021 - Create referral and send for triage](#api-Default-a021-create-referral-request-and-send-for-triage)",
        "[[HYPERLINK_A030]]": "[A030 - Retrieve e-RS business functions](#api-Default-a030-retrieve-business-functions)",
        "[[HYPERLINK_A033]]": "[A033 - Retrieve Healthcare Service](#api-Default-a033-retrieve-healthcare-service)",
        "[[HYPERLINK_A034]]": "[A034 - Retrieve service version](#api-Default-a034-retrieve-service-version)",
        "[[HYPERLINK_A035]]": "[A035 - Search for Healthcare Services](#api-Default-a035-search-for-healthcare-services)",
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
