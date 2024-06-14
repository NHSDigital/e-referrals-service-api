# Stub API Server

Stub API Server built using [apimocker](https://github.com/gstroup/apimocker) deployable as a [Apigee Hosted Target](https://docs.apigee.com/api-platform/hosted-targets/hosted-targets-overview).

Intended for "sandbox" functionality, and is the target endpoint for the hosted docs' *Try it now* functionality.

## Developing

```
make build
make run
```

 * Use the examples from the OAS (`components/examples/`) sym-linking them into the app.

## Deployment

Redeploy the API Proxy. See the main [README.md](../README.md).

## Endpoints

- [x] POST    `/STU3/ReferralRequest/$ers.createReferral`
- [x] POST    `/STU3/ReferralRequest/$ers.createReferralAndSendForTriage`
- [x] POST    `/STU3/HealthcareService/$ers.searchHealthcareServicesForPatient`
- [x] GET     `/STU3/CodeSystem/{codeSystemType}`
- [x] GET     `/STU3/Slot`
- [x] GET     `/R4/PractitionerRole`
- [x] POST    `/STU3/Binary`
- [x] POST    `/STU3/ReferralRequest/{ubrn}/$ers.generatePatientLetter`
- [x] GET     `/STU3/Binary/{attachmentLogicalID}`
- [x] GET     `/STU3/ReferralRequest/{ubrn}`
- [x] GET     `/STU3/ReferralRequest/{ubrn}/_history/{version}`
- [x] POST    `/STU3/ReferralRequest/{ubrn}/$ers.maintainReferralLetter`
- [x] POST    `/STU3/Appointment`
- [x] POST    `/STU3/ReferralRequest/{ubrn}/$ers.generateCRI`
- [x] POST    `/STU3/CommunicationRequest/{ubrn}/$ers.generateCRI`


