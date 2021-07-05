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

- [x] POST    `/STU3/v1/ReferralRequest/$ers.createReferral`
- [x] POST    `/STU3/v1/ReferralRequest/$ers.createReferralAndSendForTriage`
- [x] POST    `/STU3/v1/HealthcareService/$ers.searchHealthcareServicesForPatient`
- [x] GET     `/STU3/v1/CodeSystem/{codeSystemType}`
- [x] GET     `/STU3/v1/Slot`
- [x] GET     `/R4/v1/PractitionerRole`
- [x] POST    `/STU3/v1/Binary`
- [x] POST    `/STU3/v1/ReferralRequest/{ubrn}/$ers.generatePatientLetter`
- [x] GET     `/STU3/v1/Binary/{attachmentLogicalID}`
- [x] GET     `/STU3/v1/ReferralRequest/{ubrn}`
- [x] GET     `/STU3/v1/ReferralRequest/{ubrn}/_history/{version}`
- [x] POST    `/STU3/v1/ReferralRequest/{ubrn}/$ers.maintainReferralLetter`
- [x] POST    `/STU3/v1/Appointment`
- [x] POST    `/STU3/v1/ReferralRequest/{ubrn}/$ers.generateCRI`

