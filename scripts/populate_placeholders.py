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
      "[[HYPERLINK_A007]]": "[A007 - Retrieve clinical information](https://developer.nhs.uk/apis/e-Referrals/explore_endpoint_a007.html)",
      "[[HYPERLINK_A010]]": "[A010 - Patient service search](#api-Default-a010-patient-service-search)",
      "[[HYPERLINK_A011]]": "[A011 - Create referral](#api-Default-a011-create-referral)",
      "[[HYPERLINK_A012]]": "[A012 - Maintain referral letter](#api-Default-a012-maintain-referral-letter)",
      "[[HYPERLINK_A015]]": "[A015 - Retrieve appointment slots](#api-Default-a015-retrieve-appointment-slots)",
      "[[HYPERLINK_A016]]": "[A016 - Book or defer appointment](https://developer.nhs.uk/apis/e-Referrals/explore_endpoint_a016.html)",
      "[[HYPERLINK_A019]]": "[A019 - Generate patient letter](#api-Default-a019-generate-patient-letter)",
      "[[HYPERLINK_A020]]": "[A020 - Upload file to document store](#api-Default-a020-upload-file-to-document-store)",
      "[[HYPERLINK_A021]]": "[A021 - Create referral and send for triage](#api-Default-a021-create-referral-request-and-send-for-triage)",
      "[[HYPERLINK_PDS]]": "[Personal Demographic Service (PDS)](https://digital.nhs.uk/developer/api-catalogue/personal-demographics-service-fhir)",
      "[[HYPERLINK_ERS_BUS_FUNCTIONS]]": "[e-RS Business Functions](https://fhir.nhs.uk/CodeSystem/eRS-BusinessFunction-1)"
    }

    data = sys.stdin.read()

    for key, value in substitutes_dict.items():
        data = data.replace(key, value)

    sys.stdout.write(data)
    sys.stdout.close()


if __name__ == "__main__":
    main()
