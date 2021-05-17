
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

module.exports = {


  getExampleResponseForCreateReferral: function (request) {

    var exampleResponseMap = {
      'src/mocks/createReferral/requests/CreateReferralParameters.json': 'createReferral/responses/ReferralRequest.json',
      'src/mocks/createReferral/requests/CreateReferralParametersFull.json': 'createReferral/responses/ReferralRequest.json',
      'src/mocks/createReferral/requests/CreateReferralParametersTwentyServices.json': 'createReferral/responses/ReferralRequestTwentyServices.json'
    };

    return mapExampleResponse(request, exampleResponseMap);

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



}
