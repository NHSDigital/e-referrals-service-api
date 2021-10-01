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
      "[[HYPERLINK_A008]]": "[A008 - Retrieve referral worklist](#api-Default-a008-retrieve-worklist)",
      "[[HYPERLINK_A010]]": "[A010 - Patient service search](#api-Default-a010-patient-service-search)",
      "[[HYPERLINK_A011]]": "[A011 - Create referral](#api-Default-a011-create-referral)",
      "[[HYPERLINK_A012]]": "[A012 - Maintain referral letter](#api-Default-a012-maintain-referral-letter)",
      "[[HYPERLINK_A013]]": "[A013 - Accept referral](https://developer.nhs.uk/apis/e-Referrals/explore_endpoint_a013.html)",
      "[[HYPERLINK_A014]]": "[A014 - Reject referral](https://developer.nhs.uk/apis/e-Referrals/explore_endpoint_a014.html)",
      "[[HYPERLINK_A015]]": "[A015 - Retrieve appointment slots](#api-Default-a015-retrieve-appointment-slots)",
      "[[HYPERLINK_A016]]": "[A016 - Book or defer appointment](#api-Default-a016-book-or-defer-appointment)",
      "[[HYPERLINK_A019]]": "[A019 - Generate patient letter](#api-Default-a019-generate-patient-letter)",
      "[[HYPERLINK_A020]]": "[A020 - Upload file to document store](#api-Default-a020-upload-file-to-document-store)",
      "[[HYPERLINK_A021]]": "[A021 - Create referral and send for triage](#api-Default-a021-create-referral-request-and-send-for-triage)",
      "[[HYPERLINK_A022]]": "[A022 - Cancel appointment, action later](https://developer.nhs.uk/apis/e-Referrals/explore_endpoint_a022.html)",
      "[[HYPERLINK_A023]]": "[A023 - Retrieve advice and guidance requests worklist](#api-Default-a008-retrieve-a&g-worklist)",
      "[[HYPERLINK_A024]]": "[A024 - Retrieve advice and guidance request summary](#api-Default-a024-retrieve-advice-and-guidance)",
      "[[HYPERLINK_A025]]": "[A025 - Retrieve advice and guidance conversation](#api-Default-a025-retrieve-advice-and-guidance-conversation)",
      "[[HYPERLINK_A026]]": "[A026 - Send advice and guidance response](#api-Default-a026-send-a&g-response)",
      "[[HYPERLINK_A027]]": "[A027 - Convert advice and guidance request to referral](#api-Default-a027-convert-a&g-to-referral)",
      "[[HYPERLINK_A028]]": "[A028 - Record triage outcome](https://developer.nhs.uk/apis/e-Referrals/explore_endpoint_a028.html)",
      "[[HYPERLINK_A030]]": "[A030 - Retrieve e-RS business functions](#api-Default-a030-retrieve-business-functions)",
      "[[HYPERLINK_ONBOARDING]]": "[onboarding](#api-description__onboarding)",
      "[[HYPERLINK_STABLE]]": "[stable](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#api-status)",
      "[[HYPERLINK_BETA]]": "[beta](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#api-status)",
      "[[HYPERLINK_PDS]]": "[Personal Demographic Service (PDS)](https://digital.nhs.uk/developer/api-catalogue/personal-demographics-service-fhir)",
      "[[HYPERLINK_CIS2]]": "[CIS2](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/user-restricted-restful-apis-nhs-cis2-combined-authentication-and-authorisation)",
      "[[HYPERLINK_ERS_BUS_FUNCTIONS]]": "[e-RS Business Functions](https://fhir.nhs.uk/CodeSystem/eRS-BusinessFunction-1)"
    }

    data = sys.stdin.read()

    for key, value in substitutes_dict.items():
        data = data.replace(key, value)

    sys.stdout.write(data)
    sys.stdout.close()


if __name__ == "__main__":
    main()
