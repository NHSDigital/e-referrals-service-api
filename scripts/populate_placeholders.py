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
        "[[HYPERLINK_A004]]": "[Retrieve reference data (A004)](#get-/STU3/CodeSystem/-codeSystemType-)",
        "[[HYPERLINK_A005]]": "[Retrieve referral request (A005)](#get-/STU3/ReferralRequest/-ubrn-)",
        "[[HYPERLINK_A006]]": "[Retrieve attachment (A006)](#get-/STU3/Binary/-attachmentLogicalID-)",
        "[[HYPERLINK_A007]]": "[Retrieve clinical information (A007)](#post-/STU3/ReferralRequest/-ubrn-/$ers.generateCRI)",
        "[[HYPERLINK_A008]]": "[Retrieve referral worklist (A008)](#post-/STU3/ReferralRequest/$ers.fetchworklist)",
        "[[HYPERLINK_A010]]": "[Patient service search (A010)](#post-/STU3/HealthcareService/$ers.searchHealthcareServicesForPatient)",
        "[[HYPERLINK_A011]]": "[Create referral (A011)](#post-/STU3/ReferralRequest/$ers.createReferral)",
        "[[HYPERLINK_A012]]": "[Maintain referral letter (A012)](#post-/STU3/ReferralRequest/-ubrn-/$ers.maintainReferralLetter)",
        "[[HYPERLINK_A013]]": "[Accept referral (A013)](#post-/STU3/ReferralRequest/-ubrn-/$ers.acceptReferral)",
        "[[HYPERLINK_A014]]": "[Reject referral (A014)](#post-/STU3/ReferralRequest/-ubrn-/$ers.rejectReferral)",
        "[[HYPERLINK_A015]]": "[Retrieve appointment slots (A015)](#get-/STU3/Slot)",
        "[[HYPERLINK_A016]]": "[Book or defer appointment (A016)](#post-/STU3/Appointment)",
        "[[HYPERLINK_A019]]": "[Generate patient letter (A019)](#post-/STU3/ReferralRequest/-ubrn-/$ers.generatePatientLetter)",
        "[[HYPERLINK_A020]]": "[Upload file to document store (A020)](#post-/STU3/Binary)",
        "[[HYPERLINK_A022]]": "[Cancel appointment, action later (A022)](#post-/STU3/ReferralRequest/-ubrn-/$ers.cancelAppointmentActionLater)",
        "[[HYPERLINK_A023]]": "[Retrieve advice and guidance requests worklist (A023)](#post-/STU3/CommunicationRequest/$ers.fetchworklist)",
        "[[HYPERLINK_A024]]": "[Retrieve advice and guidance request summary (A024)](#get-/STU3/CommunicationRequest/-ubrn-)",
        "[[HYPERLINK_A025]]": "[Retrieve advice and guidance conversation (A025)](#get-/STU3/Communication)",
        "[[HYPERLINK_A026]]": "[Send advice and guidance response (A026)](#post-/STU3/CommunicationRequest/-ubrn-/$ers.sendCommunicationToRequester)",
        "[[HYPERLINK_A027]]": "[Convert advice and guidance request to referral (A027)](#post-/STU3/ReferralRequest/$ers.createFromCommunicationRequestActionLater)",
        "[[HYPERLINK_A028]]": "[Record triage outcome (A028)](#post-/STU3/ReferralRequest/-ubrn-/$ers.recordReviewOutcome)",
        "[[HYPERLINK_A029]]": "[Available actions for user (A029)](#get-/STU3/Task)",
        "[[HYPERLINK_A030]]": "[Retrieve user business functions (A030)](#get-/R4/PractitionerRole)",
        "[[HYPERLINK_A031]]": "[Change shortlist (A031)](#post-/STU3/ReferralRequest/-ubrn-/$ers.changeShortlist)",
        "[[HYPERLINK_A033]]": "[Retrieve healthcare service (A033)](#get-/R4/HealthcareService/-id-)",
        "[[HYPERLINK_A034]]": "[Update appointment (A034)](#put-/STU3/Appointment/-id-)",
        "[[HYPERLINK_A035]]": "[Search for healthcare services (A035)](#get-/R4/HealthcareService)",
        "[[HYPERLINK_A036]]": "[Cancel referral (A036)](#post-/STU3/ReferralRequest/-ubrn-/$ers.cancelReferral)",
        "[[HYPERLINK_A037]]": "[Retrieve healthcare service version (A037)](#head-/R4/HealthcareService/-id-)",
        "[[HYPERLINK_A038]]": "[Retrieve appointment (A038)](#get-/STU3/Appointment/-id-)",
        "[[HYPERLINK_A040]]": "[Retrieve “on-behalf-of” practitioner user information (A040)](#get-/R4/Practitioner)",
        "[[HYPERLINK_A041]]": "[Search for service requests (A041)](#get-/R4/ServiceRequest)",
        "[[HYPERLINK_A042]]": "[Retrieve attachment (A042)](#get-/R4/Binary/-id-)",
        "[[HYPERLINK_A043]]": "[Retrieve advice and guidance overview PDF (A043)](#post-/STU3/CommunicationRequest/-ubrn-/$ers.generateCRI)",
        "[[HYPERLINK_A044]]": "[Create advice and guidance request (A044)](#post-/STU3/CommunicationRequest/$ers.createAdviceAndGuidance)",
        "[[HYPERLINK_ONBOARDING]]": "[onboarding](#overview--onboarding)",
        "[[HYPERLINK_NETWORK_ACCESS]]": "[Network access](#overview--network-access)",
        "[[HYPERLINK_STABLE]]": "[stable](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#api-status)",
        "[[HYPERLINK_PRODUCTION]]": "[In production](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#statuses)",
        "[[HYPERLINK_PDS]]": "[Personal Demographic Service (PDS)](https://digital.nhs.uk/developer/api-catalogue/personal-demographics-service-fhir)",
        "[[HYPERLINK_CIS2]]": "[CIS2](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/user-restricted-restful-apis-nhs-cis2-combined-authentication-and-authorisation)",
        "[[HYPERLINK_ERS_BUS_FUNCTIONS]]": "[e-RS Business Functions](https://fhir.nhs.uk/CodeSystem/eRS-BusinessFunction-1)",
        "[[HYPERLINK_PERFORMANCE_TESTING]]": "[performance testing](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#performance-testing)",
        "[[HYPERLINK_CONTACT_US]]": "[contact us](https://digital.nhs.uk/developer/help-and-support)",
        "[[HYPERLINK_CIS_AUTH_SHORT]]": "[CIS2](https://digital.nhs.uk/services/identity-and-access-management/nhs-care-identity-service-2/care-identity-authentication)",
        "[[HYPERLINK_CIS_AUTH_LONG]]": "[NHS Care Identity Service 2 (CIS2)](https://digital.nhs.uk/services/identity-and-access-management/nhs-care-identity-service-2/care-identity-authentication)",
        "[[HYPERLINK_SIGNED_JWT]]": "[Signed JWT](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/application-restricted-restful-apis-signed-jwt-authentication)",
        "[[HYPERLINK_PATHWAY_START]]": "[here](https://digital.nhs.uk/services/e-referral-service/document-library/pathway-start)",
        "[[HYPERLINK_RTT_RULES]]": "[national RTT rules](https://www.gov.uk/government/publications/right-to-start-consultant-led-treatment-within-18-weeks)",
    }

    data = sys.stdin.read()

    for key, value in substitutes_dict.items():
        data = data.replace(key, value)

    sys.stdout.write(data)
    sys.stdout.close()


if __name__ == "__main__":
    main()
