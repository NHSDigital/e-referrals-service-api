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
        "[[HYPERLINK_A004]]": "[A004 - Retrieve reference data](#get-/STU3/CodeSystem/-codeSystemType-)",
        "[[HYPERLINK_A005]]": "[A005 - Retrieve referral request](#get-/STU3/ReferralRequest/-ubrn-)",
        "[[HYPERLINK_A006]]": "[A006 - Retrieve attachment](#get-/STU3/Binary/-attachmentLogicalID-)",
        "[[HYPERLINK_A007]]": "[A007 - Retrieve clinical information](#post-/STU3/ReferralRequest/-ubrn-/$ers.generateCRI)",
        "[[HYPERLINK_A008]]": "[A008 - Retrieve referral worklist](#post-/STU3/ReferralRequest/$ers.fetchworklist)",
        "[[HYPERLINK_A010]]": "[A010 - Patient service search](#post-/STU3/HealthcareService/$ers.searchHealthcareServicesForPatient)",
        "[[HYPERLINK_A011]]": "[A011 - Create referral](#post-/STU3/ReferralRequest/$ers.createReferral)",
        "[[HYPERLINK_A012]]": "[A012 - Maintain referral letter](#post-/STU3/ReferralRequest/-ubrn-/$ers.maintainReferralLetter)",
        "[[HYPERLINK_A013]]": "[A013 - Accept referral](#post-/STU3/ReferralRequest/-ubrn-/$ers.acceptReferral)",
        "[[HYPERLINK_A014]]": "[A014 - Reject referral](#post-/STU3/ReferralRequest/-ubrn-/$ers.rejectReferral)",
        "[[HYPERLINK_A015]]": "[A015 - Retrieve appointment slots](#get-/STU3/Slot)",
        "[[HYPERLINK_A016]]": "[A016 - Book or defer appointment](#post-/STU3/Appointment)",
        "[[HYPERLINK_A019]]": "[A019 - Generate patient letter](#post-/STU3/ReferralRequest/-ubrn-/$ers.generatePatientLetter)",
        "[[HYPERLINK_A020]]": "[A020 - Upload file to document store](#post-/STU3/Binary)",
        "[[HYPERLINK_A021]]": "[A021 - Create referral and send for triage](#post-/STU3/ReferralRequest/$ers.createReferralAndSendForTriage)",
        "[[HYPERLINK_A022]]": "[A022 - Cancel appointment, action later](#post-/STU3/ReferralRequest/-ubrn-/$ers.cancelAppointmentActionLater)",
        "[[HYPERLINK_A023]]": "[A023 - Retrieve advice and guidance requests worklist](#post-/STU3/CommunicationRequest/$ers.fetchworklist)",
        "[[HYPERLINK_A024]]": "[A024 - Retrieve advice and guidance request summary](#get-/STU3/CommunicationRequest/-ubrn-)",
        "[[HYPERLINK_A025]]": "[A025 - Retrieve advice and guidance conversation](#get-/STU3/Communication)",
        "[[HYPERLINK_A026]]": "[A026 - Send advice and guidance response](#post-/STU3/CommunicationRequest/-ubrn-/$ers.sendCommunicationToRequester)",
        "[[HYPERLINK_A027]]": "[A027 - Convert advice and guidance request to referral](#post-/STU3/ReferralRequest/$ers.createFromCommunicationRequestActionLater)",
        "[[HYPERLINK_A028]]": "[A028 - Record triage outcome](#post-/STU3/ReferralRequest/-ubrn-/$ers.recordReviewOutcomev)",
        "[[HYPERLINK_A029]]": "[A029 - Available actions for user list](#get-/STU3/Task)",
        "[[HYPERLINK_A030]]": "[A030 - Retrieve e-RS business functions](#get-/R4/PractitionerRole)",
        "[[HYPERLINK_A031]]": "[A031 - Change shortlist](#post-/STU3/ReferralRequest/-ubrn-/$ers.changeShortlist)",
        "[[HYPERLINK_A032]]": "[A032 - Change shortlist and send for triage](#post-/STU3/ReferralRequest/-ubrn-/$ers.changeShortlistAndSendForTriage)",
        "[[HYPERLINK_A033]]": "[A033 - Retrieve healthcare service](#get-/R4/HealthcareService/-id-)",
        "[[HYPERLINK_A034]]": "[A034 - Update appointment](#put-/STU3/Appointment/-id-)",
        "[[HYPERLINK_A035]]": "[A035 - Search for healthcare services](#get-/R4/HealthcareService)",
        "[[HYPERLINK_A036]]": "[A036 - Cancel referral](#post-/STU3/ReferralRequest/-ubrn-/$ers.cancelReferral)",
        "[[HYPERLINK_A037]]": "[A037 - Retrieve healthcare service version](#head-/R4/HealthcareService/-id-)",
        "[[HYPERLINK_A038]]": "[A038 - Retrieve appointment](#get-/STU3/Appointment/-id-)",
        "[[HYPERLINK_A040]]": "[A040 - Retrieve e-RS-Specific Practitioner Information](#get-/R4/Practitioner)",
        "[[HYPERLINK_A041]]": "[A041 - Search for service requests](#get-/R4/ServiceRequest)",
        "[[HYPERLINK_A043]]": "[A043 - Retrieve advice and guidance overview PDF](#post-/STU3/CommunicationRequest/-ubrn-/$ers.generateCRI)",
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
