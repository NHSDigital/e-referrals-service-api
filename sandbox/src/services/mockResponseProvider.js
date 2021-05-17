
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

function mapExampleGetResponse(parameterValue, exampleResponseMap) {
  for (const [requestParameter, responseBodyPath] of Object.entries(exampleResponseMap)) {
    if (parameterValue === requestParameter) {
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

    var responseMapForRC = {
      'src/mocks/createReferralAndSendForTriage/requests/Parameters.json': 'createReferralAndSendForTriage/responses/ReferralRequest.json'
    };

    var responseMapForRCA = {
      'src/mocks/createReferralAndSendForTriage/requests/ParametersWithNamedClinician.json': 'createReferralAndSendForTriage/responses/ReferralRequestWithNamedClinician.json',
    };

    const isRCBusinessRole = request.headers["nhsd-ers-business-function"] === 'REFERRING_CLINICIAN'

    return mapExampleResponse(request, isRCBusinessRole ? responseMapForRC : responseMapForRCA);

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

  },

  getExampleResponseForRetrieveAppointmentSlots: function (request) {

    const serviceId = request.query['schedule.actor:HealthcareService']
    const page = request.query['page']
    const pageSize = request.query['_count']
    const priority = request.query['appointmentType']
    const status = request.query['status']

    // paged result mocking
    if (serviceId === '11000' && priority === 'ROUTINE' && status === 'free') {
      if (pageSize === '5') {
        switch (page) {
          case '1':
          case '2':
          case '3':
          case '4':
            return { responsePath: 'retrieveAppointmentSlots/responses/Page' + page + 'PageSize5.json', responseCode: 200 }
          case '5':
            return { responsePath: 'retrieveAppointmentSlots/responses/ErrorPage5.json', responseCode: 400 }
        }
      } else if (pageSize === '10') {
        switch (page) {
          case '1':
          case '2':
            return { responsePath: 'retrieveAppointmentSlots/responses/Page' + page + 'PageSize10.json', responseCode: 200 }
        }
      }

    }

    // empty result mocking
    if (serviceId === '10000' && page === '1' && pageSize === '10' && priority === 'ROUTINE' && status === 'free') {
      return { responsePath: 'retrieveAppointmentSlots/responses/NoSlots.json', responseCode: 200 }
    }
    return {}


  }
}
