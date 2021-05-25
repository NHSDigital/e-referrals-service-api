
const fs = require('fs')
const lodash = require('lodash')

function mapExampleResponse(request, exampleResponseMap) {

  if (request != null && request.payload != null) {

    for (const [requestBodyPath, responseBodyPath] of Object.entries(exampleResponseMap)) {

      const exampleRequestBody = JSON.parse(fs.readFileSync(requestBodyPath))

      var requestBody = request.payload;
      if ('object' != (typeof requestBody)) {
        requestBody = JSON.parse(request.payload)
      }
      if (lodash.isEqual(requestBody, exampleRequestBody)) {
        return responseBodyPath;
      }
    }

  }

  return null;
}

function mapExampleGetResponse(parameterValue, exampleResponseMap){
  for (const [requestParameter, responseBodyPath] of Object.entries(exampleResponseMap)) {
    if (parameterValue === requestParameter){
      return responseBodyPath;
    }
  }
}

module.exports = {


  getExampleResponseForCreateReferral: function (request) {

    var responseMapForRC = {
      'src/mocks/createReferral/requests/MinimalRequest.json': 'createReferral/responses/ReferralRequest.json',
      'src/mocks/createReferral/requests/RequestTwentyServices.json': 'createReferral/responses/ReferralRequestTwentyServices.json'
    };

    var responseMapForRCA = {
      'src/mocks/createReferral/requests/MinimalRequestWithReferringClinician.json': 'createReferral/responses/ReferralRequest.json'
    };

    const isRCBusinessRole = request.headers["nhsd-ers-business-function"] === 'REFERRING_CLINICIAN'

    return mapExampleResponse(request, isRCBusinessRole ? responseMapForRC : responseMapForRCA);

  },

  getExampleResponseForCreateReferralAndSendForTriage: function (request) {

    var exampleResponseMap = {
      'src/mocks/createReferralAndSendForTriage/requests/Parameters.json': 'createReferralAndSendForTriage/responses/ReferralRequest.json',
      'src/mocks/createReferralAndSendForTriage/requests/ParametersWithNamedClinician.json': 'createReferralAndSendForTriage/responses/ReferralRequestWithNamedClinician.json',
    };

    return mapExampleResponse(request, exampleResponseMap);

  },


  getExampleResponseForPatientServiceSearch: function (request) {

    var exampleResponseMap = {
      'src/mocks/patientServiceSearch/requests/ParametersReturningSingleService.json': 'patientServiceSearch/responses/FetchServiceListWithSingleService.json',
      'src/mocks/patientServiceSearch/requests/ParametersReturningMultipleServices.json': 'patientServiceSearch/responses/FetchServiceListWithMultipleServices.json',
      'src/mocks/patientServiceSearch/requests/ParametersFullyPopulated.json': 'patientServiceSearch/responses/EmptyResponse.json'
    };

    return mapExampleResponse(request, exampleResponseMap);

  },

  getExampleResponseForGetCodeSystem: function (request) {

    var exampleResponseMap = {
      'SPECIALTY': 'getCodeSystem/responses/SpecialtyCodeSystem.json',
      'CLINIC-TYPE': 'getCodeSystem/responses/ClinicTypeCodeSystem.json',
      'APPOINTMENT-CANCELLATION-REASON': 'getCodeSystem/responses/AppointmentCancellationReasonCodeSystem.json',
    };

    return mapExampleGetResponse(request, exampleResponseMap);

  }



}
