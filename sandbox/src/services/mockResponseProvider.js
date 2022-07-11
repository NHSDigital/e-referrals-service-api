
const fs = require('fs')
const lodash = require('lodash')

function mapExampleResponse(request, exampleResponseMap) {

  if (request && request.payload) {
    for (const [requestBodyPath, response] of Object.entries(exampleResponseMap)) {
      try {
        const exampleRequestBody = JSON.parse(fs.readFileSync(requestBodyPath))
        var requestBody = request.payload;

        if ('object' != (typeof requestBody)) {
          requestBody = JSON.parse(request.payload)
        }

        if (lodash.isEqual(requestBody, exampleRequestBody)) {
          return response;
        }
      } catch (err) {
        console.error(err)
        throw err
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
      'REFERRAL-CANCELLATION-REASON': 'getCodeSystem/responses/ReferralCancellationReasonCodeSystem.json',
      'APPOINTMENT-NON-ATTENDANCE-REASON': 'getCodeSystem/responses/AppointmentNonAttendanceReasonCodeSystem.json',
      'PRIORITY': 'getCodeSystem/responses/PriorityCodeSystem.json'
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

  getExampleResponseForRetrieveOboUsers: function () {
    return { responsePath: 'retrieveOboUsers/responses/PractitionerBundle.json', responseCode: 200 }
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

    // Scenario 7 - ReferralRequest with additional requirements
    if (ubrn === '000000070011' && (!version || version === '5')) {
      return { responsePath: 'retrieveReferralRequest/responses/WithAdditionalRequirements.json', responseCode: 200 }
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

  putExampleResponseForUpdateAppointment: function (request) {
    var responseMap = {
      'src/mocks/updateAppointment/requests/MinimalCancellationReasonOnlyCommentNotMandatory.json': { responsePath: 'updateAppointment/responses/MinimalCancellationReasonOnlyCommentNotMandatory.json', responseCode: 200 },
      'src/mocks/updateAppointment/requests/CancellationReasonAndMandatoryComment.json': { responsePath: 'updateAppointment/responses/CancellationReasonAndMandatoryComment.json', responseCode: 200 },
      'src/mocks/updateAppointment/requests/CancellationReasonOnlyCommentMandatory.json': { responsePath: 'updateAppointment/responses/CancellationReasonOnlyCommentMandatory.json', responseCode: 422 },
      'src/mocks/updateAppointment/requests/CancellationInvalidReason.json': { responsePath: 'updateAppointment/responses/CancellationInvalidReason.json', responseCode: 422 }
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
      'src/mocks/retrieveWorklist/requests/FilteringByClinician.json': 'retrieveWorklist/responses/FilteredByClinician.json',
      'src/mocks/retrieveWorklist/requests/MinimalRejectedTriageResponse.json': 'retrieveWorklist/responses/RejectedTriageResponse.json',
      'src/mocks/retrieveWorklist/requests/MinimalAssessmentReturnedCancelledDna.json': 'retrieveWorklist/responses/AssessmentReturnedCancelledDna.json',
      'src/mocks/retrieveWorklist/requests/MinimalAwaitingBooking.json': 'retrieveWorklist/responses/AwaitingBooking.json',
      'src/mocks/retrieveWorklist/requests/MinimalLettersOutstanding.json': 'retrieveWorklist/responses/LettersOutstanding.json'
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

  getResponseForRetrieveAdviceAndGuidanceConversation: function (request) {
    const basedOn = request.query["based-on"]

    // Scenario 1 - Single message from referrer
    if (basedOn === 'CommunicationRequest/000000070000/_history/1') {
      return { responsePath: 'retrieveAdviceAndGuidanceConversation/SingleMessageFromReferrer.json', responseCode: 200, version: 1 }
    }

    // Scenario 2 - One message each way
    if (basedOn === 'CommunicationRequest/000000070000/_history/2') {
      return { responsePath: 'retrieveAdviceAndGuidanceConversation/OneMessageEachWay.json', responseCode: 200, version: 2 }
    }

    // Scenario 3 - Attachment present in each direction
    if (basedOn === 'CommunicationRequest/000000070001/_history/6') {
      return { responsePath: 'retrieveAdviceAndGuidanceConversation/AttachmentPresentInEachDirection.json', responseCode: 200, version: 6 }
    }

    // Scenario 4 -	Multi-way conversation
    if (basedOn === 'CommunicationRequest/000000070002/_history/1') {
      return { responsePath: 'retrieveAdviceAndGuidanceConversation/MultiWayConversation.json', responseCode: 200, version: 6 }
    }

    // Scenario 5 -	Attachment uploaded from RCS before A&G creation
    if (basedOn === 'CommunicationRequest/000000070003/_history/7') {
      return { responsePath: 'retrieveAdviceAndGuidanceConversation/AttachmentUploadedFromRCS.json', responseCode: 200, version: 7 }
    }

    return {}
  },

  getResponseForSendAdviceAndGuidanceResponse: function (request) {
    var responseMap = {
      'src/mocks/sendAdviceAndGuidanceResponse/requests/RequireFurtherInformation.json': 'sendAdviceAndGuidanceResponse/responses/RequireFurtherInformation.json',
      'src/mocks/sendAdviceAndGuidanceResponse/requests/ReturnToReferrerWithAdvice.json': 'sendAdviceAndGuidanceResponse/responses/ReturnToReferrerWithAdvice.json',
      'src/mocks/sendAdviceAndGuidanceResponse/requests/AttachmentIncluded.json': 'sendAdviceAndGuidanceResponse/responses/AttachmentIncluded.json'
    }

    return mapExampleResponse(request, responseMap)


  },

  getResponseForConvertAdviceAndGuidanceToReferral: function (request) {
    var responseMap = {
      'src/mocks/convertAdviceAndGuidanceToReferral/requests/NoAttachments.json': 'convertAdviceAndGuidanceToReferral/responses/NoAttachments.json',
      'src/mocks/convertAdviceAndGuidanceToReferral/requests/WithAttachments.json': 'convertAdviceAndGuidanceToReferral/responses/WithAttachments.json',
    }

    return mapExampleResponse(request, responseMap)


  },

  getResponseForRecordTriageOutcome: function (request) {
    var responseMap = {
      'src/mocks/recordTriageOutcome/requests/ReturnToReferrerWithAdvice.json': 'recordTriageOutcome/responses/ReturnToReferrerWithAdvice.json',
      'src/mocks/recordTriageOutcome/requests/AcceptReferBookLater.json': 'recordTriageOutcome/responses/AcceptReferBookLater.json',
      'src/mocks/recordTriageOutcome/requests/AttachmentIncluded.json': 'recordTriageOutcome/responses/AttachmentIncluded.json',
    }

    return mapExampleResponse(request, responseMap)


  },

  getResponseForAcceptReferral: function (request) {

    const ubrn = request.params.ubrn;

    if (ubrn === '000000070000') {
      return { responsePath: 'acceptReferral/responses/ExampleResponse.json', responseCode: 200 }
    }
    return {}

  },

  getResponseForCancelReferral: function (request) {
    var responseMap = {
      'src/mocks/cancelReferral/requests/IntendPrivateWithoutComment.json': 'cancelReferral/responses/CancelledReferralIntendPrivateWithoutComment.json',
      'src/mocks/cancelReferral/requests/PatientRequestCancellationOther.json': 'cancelReferral/responses/CancelledReferralPatientOther.json',
      'src/mocks/cancelReferral/requests/RaisedInError.json': 'cancelReferral/responses/CancelledReferralRaisedInError.json',
      'src/mocks/cancelReferral/requests/ReferrerCancellation.json': 'cancelReferral/responses/CancelledBookedReferralReferrerCancellation.json',
      'src/mocks/cancelReferral/requests/NoLongerRequired.json': 'cancelReferral/responses/CancelledReferralWithCancelledBookingNoLongerRequired.json',
      'src/mocks/cancelReferral/requests/IntendPrivateWithComment.json': 'cancelReferral/responses/CancelledReferralResolvedDeferralIntendPrivateWithComment.json'
    }

    return mapExampleResponse(request, responseMap)
  },

  getResponseForRejectReferral: function (request) {
    var responseMap = {
      'src/mocks/rejectReferral/requests/BasicExampleIbs.json': 'rejectReferral/responses/ExampleResponseIbs.json',
      'src/mocks/rejectReferral/requests/BasicExampleDbs.json': 'rejectReferral/responses/ExampleResponseDbs.json'
    }

    return mapExampleResponse(request, responseMap)
  },

  getResponseForAvailableActionsForUserList: function (request) {

    const focus = request.query['focus']
    const intent = request.query['intent']
    const status = request.query['status']

    // Scenario 1 No "action" is available - A empty list is returned to the caller indicating there are no "actions" available currently
    if (focus === 'ReferralRequest/000000070000/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'availableActionsForUserList/Empty.json'
    }

    // Scenario 2 An "action" is available - Illustrate success response to caller
    if (focus === 'ReferralRequest/000000070001/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'availableActionsForUserList/WithRecordReviewOutcome.json'
    }

    if (focus === 'ReferralRequest/000000070002/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'availableActionsForUserList/WithCreateAppointment.json'
    }

    if (focus === 'ReferralRequest/000000070003/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'availableActionsForUserList/WithChangeShortlist.json'
    }

    if (focus === 'ReferralRequest/000000070004/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'availableActionsForUserList/WithChangeShortlistAndSendForTriage.json'
    }

    if (focus === 'ReferralRequest/000000070005/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'availableActionsForUserList/WithCancelReferral.json'
    }

    if (focus === 'ReferralRequest/000000070006/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'availableActionsForUserList/WithCancelDBAppointment.json'
    }
  },

  getResponseForCancelAppointmentActionLater: function (request) {
    var responseMap = {
      'src/mocks/cancelAppointmentActionLater/requests/MinimalExampleDBS.json': 'cancelAppointmentActionLater/responses/MinimalExampleDBS.json',
      'src/mocks/cancelAppointmentActionLater/requests/PriorityChangeAndWithAttachmentsDBS.json': 'cancelAppointmentActionLater/responses/PriorityChangeAndWithAttachmentsDBS.json',
      'src/mocks/cancelAppointmentActionLater/requests/MinimalExampleIBS.json': 'cancelAppointmentActionLater/responses/MinimalExampleIBS.json',
    }

    return mapExampleResponse(request, responseMap)


  },

  getExampleResponseForGetHealthcareService: function (request) {
    const version = request.params.version
    const serviceId = request.params.serviceId

    if (serviceId == 1 && (!version || version == 1)) {
      return 'getService/responses/sampleServiceWithMinimumAttributes.json'
    }

    if (serviceId == 2 && (!version || version == 1)) {
      return 'getService/responses/sampleServiceWithFullAttributes.json'
    }

    return null
  },

  getExampleResponseForSearchForHealthcareServices: function (request) {
    const ids = request.query['_id']

    if (ids == ['1', '2']) {
      return 'searchForServices/responses/searchServiceWithMinmumalAttributes.json'
    }

    if (ids == ['3', '4']) {
      return 'searchForServices/responses/searchServiceWithMaxAndMinlAttributes.json'
    }

    if (ids == ['5', '6']) {
      return 'searchForServices/responses/searchServiceWithEmptyResponse.json'
    }

    return null
  },

  getExampleResponseForChangeShortlist: function (request) {
    var responseMap = {
      'src/mocks/changeShortlist/requests/UnbookedReferral.json': 'changeShortlist/responses/UnbookedReferral.json',
      'src/mocks/changeShortlist/requests/UnbookedReferralMultipleServices.json': 'changeShortlist/responses/UnbookedReferralMultipleServices.json'
    }

    return mapExampleResponse(request, responseMap)
  },

  getExampleResponseForChangeShortlistAndSendForTriage: function (request) {
    var responseMap = {
      'src/mocks/changeShortlistAndSendForTriage/requests/MinimalRequest.json': 'changeShortlistAndSendForTriage/responses/MinimalRequest.json'
    }

    return mapExampleResponse(request, responseMap)
  },

  getExampleResponseForRetrieveAppointment: function (request) {
    const id = request.params.id;
    const version = request.params.version

    // Scenario 1 - Booked to directly-bookable service
    if (id === '70000' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAppointment/responses/BookedDBS.json', responseCode: 200 }
    }

    // Scenario 2 - Booked to indirectly-bookable service
    if (id === '70001' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAppointment/responses/BookedIBS.json', responseCode: 200 }
    }

    // Scenario 3 - Appointment Deferral
    if (id === '70002' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAppointment/responses/AppointmentDeferral.json', responseCode: 200 }
    }

    // Scenario 4 -	Triage Deferral
    if (id === '70003' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAppointment/responses/TriageDeferral.json', responseCode: 200 }
    }

    // Scenario 5 -	Triage Response
    if (id === '70004' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAppointment/responses/TriageResponse.json', responseCode: 200 }
    }

    // Scenario 6 -	Cancel Appointment Action Later
    if (id === '70005' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAppointment/responses/CAAL.json', responseCode: 200 }
    }

    // Scenario 7 -	Cancelled
    if (id === '70006' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAppointment/responses/Cancelled.json', responseCode: 200 }
    }

    // Scenario 8 -	Converted from A and G and Booked to DBS
    if (id === '70007' && (version === undefined || version === '5')) {
      return { responsePath: 'retrieveAppointment/responses/AandGConvertedToDBS.json', responseCode: 200 }
    }

    return {}
  },

  getExampleResponseForCreateServiceRequest: function (request) {
    const responseMap = {
      'src/mocks/r4/createServiceRequest/requests/createInitialA&G.json': 'r4/createServiceRequest/responses/createInitialA&G.json'
    };

    return mapExampleResponse(request, responseMap);
  },

  getExampleResponseForCreateQuestionnaireResponse: function (request) {
    const responseMap = {
      'src/mocks/r4/createQuestionnaireResponse/requests/createA&GShortlist.json': 'r4/createQuestionnaireResponse/responses/createA&GShortlist.json'
    };

    return mapExampleResponse(request, responseMap);
  },

  getExampleResponseForGetServiceRequest: function (request) {
    const id = request.params.id;
    if (id === 'a.4f32ed10-026e-4d01-984f-df5542673503') {
      const version = request.params.version;
      switch (version) {
        case '1':
          return { path: 'r4/getServiceRequest/responses/initialA&G.json', version: '1' };
        case '2':
        case undefined:
          return { path: 'r4/getServiceRequest/responses/A&GWithShortlist.json', version: '2' };
      }
    }

    return null;
  },

  getExampleResponseForCreateCommunication: function (request) {
    const responseMap = {
      "src/mocks/r4/createCommunication/requests/initialSPCResponse.json": "r4/createCommunication/responses/initialSPCResponse.json",
      "src/mocks/r4/createCommunication/requests/RCRespondsWithExtraDetails.json": "r4/createCommunication/responses/RCRespondsWithExtraDetails.json"
    };

    return mapExampleResponse(request, responseMap);
  },

  getExampleResponseForCreateDocumentReference: function (request) {
    const responseMap = {
      'src/mocks/r4/createDocumentReference/requests/initialA&GFile.json': 'r4/createDocumentReference/responses/initialA&GFile.json'
    };

    return mapExampleResponse(request, responseMap);
  },

  getExampleResponseForGeneratePresignedUrl: function (request) {
    const id = request.params.id;

    if (id === '4f32ed10-026e-4d01-984f-df5542673503') {
      return 'r4/generateUploadUrl/responses/generateUploadUrl.json';
    }

    return null;
  },

  getExampleResponseForSearchForCommunication: function (request) {
    const basedOn = request.query['based-on'];
    if (basedOn) {
      switch (basedOn) {
        case 'ServiceRequest/a.4f32ed10-026e-4d01-984f-df5542673503':
        case 'a.4f32ed10-026e-4d01-984f-df5542673503':
          return 'r4/searchForCommunications/responses/A&GConversation.json';
      }
    }

    return null;
  },

  getExampleResponseForGetCommunication: function (request) {
    const id = request.params.id;
    const version = request.params.version;

    if (id === '10486214-fe62-4c00-b56f-f91e5c6c13fa' && (!version || version === '1')) {
      return 'r4/getCommunication/responses/initialSPCResponse.json';
    }
    if (id === 'b6933869-5234-40da-8083-6d65b27057dd' && (!version || version === '1')) {
      return 'r4/getCommunication/responses/RCRespondsWithExtraDetails.json';
    }

    return null;
  }
}
