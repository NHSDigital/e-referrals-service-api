
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

    var responseMapForRC = {
      'src/mocks/patientServiceSearch/requests/RcMinimal.json': 'patientServiceSearch/responses/FetchServiceListWithMultipleServices.json',
      'src/mocks/patientServiceSearch/requests/RcSearchByClinicalTerm.json': 'patientServiceSearch/responses/EmptyResponse.json',
      'src/mocks/patientServiceSearch/requests/RcSearchByNamedClinician.json': 'patientServiceSearch/responses/FetchServiceListWithSingleService.json'
    };

    var responseMapForRCA = {
      'src/mocks/patientServiceSearch/requests/RcaWithIWT.json': 'patientServiceSearch/responses/FetchServiceListWithSingleService.json'
    };

    const isRCBusinessRole = request.headers["nhsd-ers-business-function"] === 'REFERRING_CLINICIAN'

    return mapExampleResponse(request, isRCBusinessRole ? responseMapForRC : responseMapForRCA);

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
    const clinicianId = request.query['schedule.actor:Practitioner']
    const page = request.query['page']
    const pageSize = request.query['_count']
    const priority = request.query['appointmentType']
    const status = request.query['status']

    // Scenario 1 Minimum slot search
    if (serviceId === '12000' && priority === 'ROUTINE' && status === 'free' && pageSize === '20' && page == 1) {

      return { responsePath: 'retrieveAppointmentSlots/responses/Minimum.json', responseCode: 200 }
    }

    // Scenario 2 Empty slot search response
    if (serviceId === '10000' && priority === 'ROUTINE' && status === 'free' && pageSize === '20' && page == 1) {

      return { responsePath: 'retrieveAppointmentSlots/responses/NoSlots.json', responseCode: 200 }
    }
    // Scenario 3, 4
    // Multipage slot search (page 1)
    // Multipage slot search (page 2)
    if (serviceId === '11000' && priority === 'ROUTINE' && status === 'free') {
      if (pageSize === '5') {
        switch (page) {
          case '1':
          case '2':
            return { responsePath: 'retrieveAppointmentSlots/responses/Page' + page + 'PageSize5.json', responseCode: 200 }
          case '5':
            return { responsePath: 'retrieveAppointmentSlots/responses/ErrorPage5.json', responseCode: 400 }
        }
      }

    }

    // Scenario 5 Multi schedule response
    if (serviceId === '13000' && priority === 'ROUTINE' && status === 'free' && pageSize === '5' && page == 1) {
      return { responsePath: 'retrieveAppointmentSlots/responses/Page1With2Schedules.json', responseCode: 200 }
    }

    // Scenario 6 Slot clinician search
    if (clinicianId === '921600556514' && serviceId === '14000' && priority === 'ROUTINE' && status === 'free' && pageSize === '5' && page == 1) {
      return { responsePath: 'retrieveAppointmentSlots/responses/SlotClinicianSearch.json', responseCode: 200 }
    }

    return {}


  },

  getExampleResponseForRetrieveBusinessFunctions: function () {

    return { responsePath: 'retrieveBusinessFunctions/responses/PractitionerRoleBundle.json', responseCode: 200 }
  },


  getExampleResponseForGeneratePatientLetter: function () {

    return { responsePath: 'generatePatientLetter/responses/000000070000_Appointment_Confirmation_Summary_20210603121353.pdf', filename: '000000070000_Appointment_Confirmation_Summary_20210603121353.pdf', responseCode: 200 }
  },

  getExampleResponseForRetrieveAttachment: function (request) {

    if (request.params.attachmentLogicalID && request.params.attachmentLogicalID.startsWith('att-')) {
      return { responsePath: 'retrieveAttachment/responses/example_attachment.pdf', filename: 'example_attachment.pdf', responseCode: 200 }
    }

  },

  getExampleResponseForRetrieveReferralRequest: function (request) {
    const ubrn = request.params.ubrn;
    const version = request.params.version

    // Scenario 1 - Unbooked ReferralRequest
    if (ubrn === '000000070000' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveReferralRequest/responses/Unbooked.json', responseCode: 200 }
    }

    // Scenario 2 - ReferralRequest booked to directly-bookable service
    if (ubrn === '000000070001' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveReferralRequest/responses/BookedDBS.json', responseCode: 200 }
    }

    // Scenario 3 - ReferralRequest booked to indirectly-bookable service
    if (ubrn === '000000070002' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveReferralRequest/responses/BookedIBS.json', responseCode: 200 }
    }

    // Scenario 4 -	ReferralRequest deferred to service provider for booking
    if (ubrn === '000000070003' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveReferralRequest/responses/DeferredToProvider.json', responseCode: 200 }
    }

    // Scenario 5 -	ReferralRequest that was converted from an Advice and Guidance Request
    if (ubrn === '000000070004' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveReferralRequest/responses/ConvertedFromAdviceAndGuidance.json', responseCode: 200 }
    }

    // Scenario 6 -	ReferralRequest with related ReferralRequest
    if (ubrn === '000000070005' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveReferralRequest/responses/WithRelatedReferral.json', responseCode: 200 }
    }

    return {}
  },

  getExampleResponseForMaintainReferralLetter: function (request) {
    const ubrn = request.params.ubrn;
    // Scenario 1 - Add clinical information for first time (single file)
    if (ubrn === '000000070000') {
      return mapExampleResponse(request, { 'src/mocks/maintainReferralLetter/requests/SingleDocumentReference.json': 'maintainReferralLetter/responses/ReferralRequestWithSingleDocumentReference.json' })
    }

    // Scenario 2 - Add clinical information for first time (two files)
    // Scenario 3 - Update clinical information
    if (ubrn === '000000070001') {
      var responseMap = {
        'src/mocks/maintainReferralLetter/requests/MultipleDocumentReferences.json': 'maintainReferralLetter/responses/ReferralRequestWithMultipleDocumentReferences.json',
        'src/mocks/maintainReferralLetter/requests/UpdateClinicalInfo.json': 'maintainReferralLetter/responses/ReferralRequestWithUpdatedDocumentReferences.json'
      };

      return mapExampleResponse(request, responseMap)
    }

    return {}

  },

  getExampleResponseForBookOrDeferAppointment: function (request) {
    var responseMap = {
      'src/mocks/bookOrDeferAppointment/requests/MinimalBooking.json': 'bookOrDeferAppointment/responses/MinimalBooking.json',
      'src/mocks/bookOrDeferAppointment/requests/MinimalDeferral.json': 'bookOrDeferAppointment/responses/MinimalDeferral.json',
      'src/mocks/bookOrDeferAppointment/requests/BookingWithNamedClinician.json': 'bookOrDeferAppointment/responses/BookingWithNamedClinician.json',
      'src/mocks/bookOrDeferAppointment/requests/DeferralWithSlotReference.json': 'bookOrDeferAppointment/responses/DeferralWithSlotReference.json',
      'src/mocks/bookOrDeferAppointment/requests/DeferralBookingAttemptProblem.json': 'bookOrDeferAppointment/responses/DeferralBookingAttemptProblem.json'
    }

    return mapExampleResponse(request, responseMap)


  },

  getExampleResponseForRetrieveClinicalInformation: function () {
    return { responsePath: 'retrieveClinicalInformation/responses/000000070000_Clinical_Information_Summary_20210706114852.pdf', filename: '000000070000_Clinical_Information_Summary_20210706114852.pdf', responseCode: 200 }
  },

  getExampleResponseForRetrieveWorklist: function (request) {
    var responseMap = {
      'src/mocks/retrieveWorklist/requests/MinimalReferralsForReview.json': 'retrieveWorklist/responses/ReferralsForReview.json',
      'src/mocks/retrieveWorklist/requests/MinimalAppointmentSlotIssues.json': 'retrieveWorklist/responses/AppointmentSlotIssues.json',
      'src/mocks/retrieveWorklist/requests/FilteringBySpecialty.json': 'retrieveWorklist/responses/FilteredBySpecialty.json',
      'src/mocks/retrieveWorklist/requests/FilteringByClinician.json': 'retrieveWorklist/responses/FilteredByClinician.json'
    }

    return mapExampleResponse(request, responseMap)


  },

  getExampleResponseForRetrieveAdviceAndGuidanceWorklist: function (request) {
    var responseMap = {
      'src/mocks/retrieveAdviceAndGuidanceWorklist/requests/MinimalAdviceAndGuidanceRequests.json': 'retrieveAdviceAndGuidanceWorklist/responses/AdviceAndGuidanceRequests.json'
    }

    return mapExampleResponse(request, responseMap)


  },

  getResponseForRetrieveAdviceAndGuidanceRequest: function (request) {
    const ubrn = request.params.ubrn;
    const version = request.params.version

    // Scenario 1 - Minimum example
    if (ubrn === '000000070000' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAdviceAndGuidanceRequest/responses/MinimalExample.json', responseCode: 200 }
    }

    // Scenario 2 - With attachment file reference
    if (ubrn === '000000070001' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAdviceAndGuidanceRequest/responses/WithAttachmentFileReference.json', responseCode: 200 }
    }

    return {}
  },

}
