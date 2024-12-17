
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
      'src/mocks/stu3/createReferral/requests/MinimalRequest.json': 'stu3/createReferral/responses/ReferralRequest.json',
      'src/mocks/stu3/createReferral/requests/RequestTwentyServices.json': 'stu3/createReferral/responses/ReferralRequestTwentyServices.json',
      'src/mocks/stu3/createReferral/requests/RequestMixedShortlist.json': 'stu3/createReferral/responses/ReferralRequestMixedShortlist.json'
    };

    var responseMapForRCA = {
      'src/mocks/stu3/createReferral/requests/MinimalRequestWithReferringClinician.json': 'stu3/createReferral/responses/ReferralRequest.json'
    };

    const isRCBusinessRole = request.headers["nhsd-ers-business-function"] === 'REFERRING_CLINICIAN'

    return mapExampleResponse(request, isRCBusinessRole ? responseMapForRC : responseMapForRCA);

  },

  getExampleResponseForCreateReferralAndSendForTriage: function (request) {

    var responseMapForRC = {
      'src/mocks/stu3/createReferralAndSendForTriage/requests/Parameters.json': 'stu3/createReferralAndSendForTriage/responses/ReferralRequest.json'
    };

    var responseMapForRCA = {
      'src/mocks/stu3/createReferralAndSendForTriage/requests/ParametersWithNamedClinician.json': 'stu3/createReferralAndSendForTriage/responses/ReferralRequestWithNamedClinician.json',
    };

    const isRCBusinessRole = request.headers["nhsd-ers-business-function"] === 'REFERRING_CLINICIAN'

    return mapExampleResponse(request, isRCBusinessRole ? responseMapForRC : responseMapForRCA);

  },


  getExampleResponseForPatientServiceSearch: function (request) {

    var responseMapForRC = {
      'src/mocks/stu3/patientServiceSearch/requests/RcMinimal.json': 'stu3/patientServiceSearch/responses/FetchServiceListWithMultipleServices.json',
      'src/mocks/stu3/patientServiceSearch/requests/RcSearchByClinicalTerm.json': 'stu3/patientServiceSearch/responses/EmptyResponse.json',
      'src/mocks/stu3/patientServiceSearch/requests/RcSearchByNamedClinician.json': 'stu3/patientServiceSearch/responses/FetchServiceListWithSingleService.json',
      'src/mocks/stu3/patientServiceSearch/requests/RcSearchForAdviceService.json': 'stu3/patientServiceSearch/responses/AdviceServiceSearch.json',
      'src/mocks/stu3/patientServiceSearch/requests/RcSearchWithCommissioningRuleOrganisation.json': 'stu3/patientServiceSearch/responses/FetchServiceListWithMultipleServices.json'
    };

    var responseMapForRCA = {
      'src/mocks/stu3/patientServiceSearch/requests/RcaWithIWT.json': 'stu3/patientServiceSearch/responses/FetchServiceListWithSingleService.json'
    };

    const isRCBusinessRole = request.headers["nhsd-ers-business-function"] === 'REFERRING_CLINICIAN'

    return mapExampleResponse(request, isRCBusinessRole ? responseMapForRC : responseMapForRCA);

  },

  getExampleResponseForGetCodeSystem: function (request) {

    var exampleResponseMap = {
      'SPECIALTY': 'stu3/getCodeSystem/responses/SpecialtyCodeSystem.json',
      'CLINIC-TYPE': 'stu3/getCodeSystem/responses/ClinicTypeCodeSystem.json',
      'APPOINTMENT-CANCELLATION-REASON': 'stu3/getCodeSystem/responses/AppointmentCancellationReasonCodeSystem.json',
      'REFERRAL-CANCELLATION-REASON': 'stu3/getCodeSystem/responses/ReferralCancellationReasonCodeSystem.json',
      'APPOINTMENT-NON-ATTENDANCE-REASON': 'stu3/getCodeSystem/responses/AppointmentNonAttendanceReasonCodeSystem.json',
      'PRIORITY': 'stu3/getCodeSystem/responses/PriorityCodeSystem.json'
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

      return { responsePath: 'stu3/retrieveAppointmentSlots/responses/Minimum.json', responseCode: 200 }
    }

    // Scenario 2 Empty slot search response
    if (serviceId === '10000' && priority === 'ROUTINE' && status === 'free' && pageSize === '20' && page == 1) {

      return { responsePath: 'stu3/retrieveAppointmentSlots/responses/NoSlots.json', responseCode: 200 }
    }
    // Scenario 3, 4
    // Multipage slot search (page 1)
    // Multipage slot search (page 2)
    if (serviceId === '11000' && priority === 'ROUTINE' && status === 'free') {
      if (pageSize === '5') {
        switch (page) {
          case '1':
          case '2':
            return { responsePath: 'stu3/retrieveAppointmentSlots/responses/Page' + page + 'PageSize5.json', responseCode: 200 }
          case '5':
            return { responsePath: 'stu3/retrieveAppointmentSlots/responses/ErrorPage5.json', responseCode: 400 }
        }
      }

    }

    // Scenario 5 Multi schedule response
    if (serviceId === '13000' && priority === 'ROUTINE' && status === 'free' && pageSize === '5' && page == 1) {
      return { responsePath: 'stu3/retrieveAppointmentSlots/responses/Page1With2Schedules.json', responseCode: 200 }
    }

    // Scenario 6 Slot clinician search
    if (clinicianId === '921600556514' && serviceId === '14000' && priority === 'ROUTINE' && status === 'free' && pageSize === '5' && page == 1) {
      return { responsePath: 'stu3/retrieveAppointmentSlots/responses/SlotClinicianSearch.json', responseCode: 200 }
    }

    return {}


  },

  getExampleResponseForGeneratePatientLetter: function () {

    return { responsePath: 'stu3/generatePatientLetter/responses/000000070000_Appointment_Confirmation_Summary_20210603121353.pdf', filename: '000000070000_Appointment_Confirmation_Summary_20210603121353.pdf', responseCode: 200 }
  },

  getExampleResponseForRetrieveAttachment: function (request) {

    const attachmentId = request.params.attachmentLogicalID;

    if (attachmentId) {
      
      if (attachmentId.startsWith('att-')) {
        return { responsePath: 'stu3/retrieveAttachment/responses/example_attachment.pdf', filename: 'example_attachment.pdf', responseCode: 200 };
      }
      
      if (this.isvalidUuid(attachmentId)) {
        return { responsePath: 'stu3/retrieveAttachment/responses/example_attachment.pdf', filename: 'example_attachment.pdf', responseCode: 200 };
      }
    }

    return {};
  },

  isvalidUuid: function(string) {
    return /^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i.test(string);
  },

  getExampleResponseForRetrieveReferralRequest: function (request) {
    const ubrn = request.params.ubrn;
    const version = request.params.version

    // Scenario 1 - Unbooked ReferralRequest
    if (ubrn === '000000070000' && (version === undefined || version === '5')) {
      return { responsePath: 'stu3/retrieveReferralRequest/responses/Unbooked.json', responseCode: 200 }
    }

    // Scenario 2 - ReferralRequest booked to directly-bookable service
    if (ubrn === '000000070001' && (version === undefined || version === '5')) {
      return { responsePath: 'stu3/retrieveReferralRequest/responses/BookedDBS.json', responseCode: 200 }
    }

    // Scenario 3 - ReferralRequest booked to indirectly-bookable service
    if (ubrn === '000000070002' && (version === undefined || version === '5')) {
      return { responsePath: 'stu3/retrieveReferralRequest/responses/BookedIBS.json', responseCode: 200 }
    }

    // Scenario 4 -	ReferralRequest deferred to service provider for booking
    if (ubrn === '000000070003' && (version === undefined || version === '5')) {
      return { responsePath: 'stu3/retrieveReferralRequest/responses/DeferredToProvider.json', responseCode: 200 }
    }

    // Scenario 5 -	ReferralRequest that was converted from an Advice and Guidance Request
    if (ubrn === '000000070004' && (version === undefined || version === '5')) {
      return { responsePath: 'stu3/retrieveReferralRequest/responses/ConvertedFromAdviceAndGuidance.json', responseCode: 200 }
    }

    // Scenario 6 -	ReferralRequest with related ReferralRequest
    if (ubrn === '000000070005' && (version === undefined || version === '5')) {
      return { responsePath: 'stu3/retrieveReferralRequest/responses/WithRelatedReferral.json', responseCode: 200 }
    }

    // Scenario 7 - ReferralRequest with additional requirements
    if (ubrn === '000000070011' && (!version || version === '5')) {
      return { responsePath: 'stu3/retrieveReferralRequest/responses/WithAdditionalRequirements.json', responseCode: 200 }
    }

    return {}
  },

  getExampleResponseForMaintainReferralLetter: function (request) {
    const ubrn = request.params.ubrn;
    // Scenario 1 - Add clinical information for first time (single file)
    if (ubrn === '000000070000') {
      return mapExampleResponse(request, { 'src/mocks/stu3/maintainReferralLetter/requests/SingleDocumentReference.json': 'stu3/maintainReferralLetter/responses/ReferralRequestWithSingleDocumentReference.json' })
    }

    // Scenario 2 - Add clinical information for first time (two files)
    // Scenario 3 - Update clinical information
    if (ubrn === '000000070001') {
      var responseMap = {
        'src/mocks/stu3/maintainReferralLetter/requests/MultipleDocumentReferences.json': 'stu3/maintainReferralLetter/responses/ReferralRequestWithMultipleDocumentReferences.json',
        'src/mocks/stu3/maintainReferralLetter/requests/UpdateClinicalInfo.json': 'stu3/maintainReferralLetter/responses/ReferralRequestWithUpdatedDocumentReferences.json'
      };

      return mapExampleResponse(request, responseMap)
    }

    return {}

  },

  getExampleResponseForBookOrDeferAppointment: function (request) {
    var responseMap = {
      'src/mocks/stu3/bookOrDeferAppointment/requests/MinimalBooking.json': 'stu3/bookOrDeferAppointment/responses/MinimalBooking.json',
      'src/mocks/stu3/bookOrDeferAppointment/requests/MinimalDeferral.json': 'stu3/bookOrDeferAppointment/responses/MinimalDeferral.json',
      'src/mocks/stu3/bookOrDeferAppointment/requests/TriageDeferral.json': 'stu3/bookOrDeferAppointment/responses/TriageDeferral.json',
      'src/mocks/stu3/bookOrDeferAppointment/requests/BookingWithNamedClinician.json': 'stu3/bookOrDeferAppointment/responses/BookingWithNamedClinician.json',
      'src/mocks/stu3/bookOrDeferAppointment/requests/DeferralWithSlotReference.json': 'stu3/bookOrDeferAppointment/responses/DeferralWithSlotReference.json',
      'src/mocks/stu3/bookOrDeferAppointment/requests/DeferralBookingAttemptProblem.json': 'stu3/bookOrDeferAppointment/responses/DeferralBookingAttemptProblem.json'
    }

    return mapExampleResponse(request, responseMap)


  },

  putExampleResponseForUpdateAppointment: function (request) {
    var responseMap = {
          'src/mocks/stu3/updateAppointment/requests/MinimalCancellationReasonOnlyCommentNotMandatory.json': {responsePath: 'stu3/updateAppointment/responses/MinimalCancellationReasonOnlyCommentNotMandatory.json', responseCode: 200},
          'src/mocks/stu3/updateAppointment/requests/CancellationReasonAndMandatoryComment.json': {responsePath: 'stu3/updateAppointment/responses/CancellationReasonAndMandatoryComment.json', responseCode: 200},
          'src/mocks/stu3/updateAppointment/requests/CancellationReasonOnlyCommentMandatory.json': {responsePath: 'stu3/updateAppointment/responses/CancellationReasonOnlyCommentMandatory.json', responseCode: 422},
          'src/mocks/stu3/updateAppointment/requests/CancellationInvalidReason.json': {responsePath: 'stu3/updateAppointment/responses/CancellationInvalidReason.json', responseCode: 422}
    }
    return mapExampleResponse(request, responseMap)
  },

  getExampleResponseForRetrieveClinicalInformation: function () {
    return { responsePath: 'stu3/retrieveClinicalInformation/responses/000000070000_Clinical_Information_Summary_20210706114852.pdf', filename: '000000070000_Clinical_Information_Summary_20210706114852.pdf', responseCode: 200 }
  },

  getExampleResponseForRetrieveAdviceAndGuidanceOverviewPdf: function () {
    return { responsePath: 'stu3/retrieveAdviceAndGuidanceOverviewPdf/responses/000049146177_Advice_And_Guidance_20220610143044.pdf', filename: '000049146177_Advice_And_Guidance_20220610143044.pdf', responseCode: 200 }
  },                      

  getExampleResponseForRetrieveWorklist: function (request) {
    var responseMap = {
      'src/mocks/stu3/retrieveWorklist/requests/MinimalReferralsForReview.json': 'stu3/retrieveWorklist/responses/ReferralsForReview.json',
      'src/mocks/stu3/retrieveWorklist/requests/MinimalAppointmentSlotIssues.json': 'stu3/retrieveWorklist/responses/AppointmentSlotIssues.json',
      'src/mocks/stu3/retrieveWorklist/requests/FilteringBySpecialty.json': 'stu3/retrieveWorklist/responses/FilteredBySpecialty.json',
      'src/mocks/stu3/retrieveWorklist/requests/FilteringByClinician.json': 'stu3/retrieveWorklist/responses/FilteredByClinician.json',
      'src/mocks/stu3/retrieveWorklist/requests/MinimalRejectedTriageResponse.json': 'stu3/retrieveWorklist/responses/RejectedTriageResponse.json',
      'src/mocks/stu3/retrieveWorklist/requests/MinimalAssessmentReturnedCancelledDna.json': 'stu3/retrieveWorklist/responses/AssessmentReturnedCancelledDna.json',
      'src/mocks/stu3/retrieveWorklist/requests/MinimalAwaitingBooking.json': 'stu3/retrieveWorklist/responses/AwaitingBooking.json',
      'src/mocks/stu3/retrieveWorklist/requests/MinimalLettersOutstanding.json': 'stu3/retrieveWorklist/responses/LettersOutstanding.json'
    }

    return mapExampleResponse(request, responseMap)


  },

  getExampleResponseForRetrieveAdviceAndGuidanceWorklist: function (request) {
    var responseMap = {
      'src/mocks/stu3/retrieveAdviceAndGuidanceWorklist/requests/MinimalAdviceAndGuidanceRequests.json': 'stu3/retrieveAdviceAndGuidanceWorklist/responses/AdviceAndGuidanceRequests.json'
    }

    return mapExampleResponse(request, responseMap)


  },

  getResponseForRetrieveAdviceAndGuidanceRequest: function (request) {
    const ubrn = request.params.ubrn;
    const version = request.params.version

    // Scenario 1 - Minimum example
    if (ubrn === '000000070000' && (version === undefined || version === '5')) {
      return { responsePath: 'stu3/retrieveAdviceAndGuidanceRequest/responses/MinimalExample.json', responseCode: 200 }
    }

    // Scenario 2 - With attachment file reference
    if (ubrn === '000000070001' && (version === undefined || version === '5')) {
      return { responsePath: 'stu3/retrieveAdviceAndGuidanceRequest/responses/WithAttachmentFileReference.json', responseCode: 200 }
    }

    return {}
  },

  getResponseForRetrieveAdviceAndGuidanceConversation: function (request) {
    const basedOn = request.query["based-on"]

    // Scenario 1 - Single message from referrer
    if (basedOn === 'CommunicationRequest/000000070000/_history/1') {
      return { responsePath: 'stu3/retrieveAdviceAndGuidanceConversation/SingleMessageFromReferrer.json', responseCode: 200, version: 1 }
    }

    // Scenario 2 - One message each way
    if (basedOn === 'CommunicationRequest/000000070000/_history/2') {
      return { responsePath: 'stu3/retrieveAdviceAndGuidanceConversation/OneMessageEachWay.json', responseCode: 200, version: 2 }
    }

    // Scenario 3 - Attachment present in each direction
    if (basedOn === 'CommunicationRequest/000000070001/_history/6') {
      return { responsePath: 'stu3/retrieveAdviceAndGuidanceConversation/AttachmentPresentInEachDirection.json', responseCode: 200, version: 6 }
    }

    // Scenario 4 -	Multi-way conversation
    if (basedOn === 'CommunicationRequest/000000070002/_history/1') {
      return { responsePath: 'stu3/retrieveAdviceAndGuidanceConversation/MultiWayConversation.json', responseCode: 200, version: 6 }
    }

    // Scenario 5 -	Attachment uploaded from RCS before A&G creation
    if (basedOn === 'CommunicationRequest/000000070003/_history/7') {
      return { responsePath: 'stu3/retrieveAdviceAndGuidanceConversation/AttachmentUploadedFromRCS.json', responseCode: 200, version: 7 }
    }

    return {}
  },

  getResponseForSendAdviceAndGuidanceResponse: function (request) {
    var responseMap = {
      'src/mocks/stu3/sendAdviceAndGuidanceResponse/requests/RequireFurtherInformation.json': 'stu3/sendAdviceAndGuidanceResponse/responses/RequireFurtherInformation.json',
      'src/mocks/stu3/sendAdviceAndGuidanceResponse/requests/ReturnToReferrerWithAdvice.json': 'stu3/sendAdviceAndGuidanceResponse/responses/ReturnToReferrerWithAdvice.json',
      'src/mocks/stu3/sendAdviceAndGuidanceResponse/requests/AttachmentIncluded.json': 'stu3/sendAdviceAndGuidanceResponse/responses/AttachmentIncluded.json'
    }

    return mapExampleResponse(request, responseMap)


  },

  getResponseForConvertAdviceAndGuidanceToReferral: function (request) {
    var responseMap = {
      'src/mocks/stu3/convertAdviceAndGuidanceToReferral/requests/NoAttachments.json': 'stu3/convertAdviceAndGuidanceToReferral/responses/NoAttachments.json',
      'src/mocks/stu3/convertAdviceAndGuidanceToReferral/requests/WithAttachments.json': 'stu3/convertAdviceAndGuidanceToReferral/responses/WithAttachments.json',
    }

    return mapExampleResponse(request, responseMap)


  },

  getResponseForRecordTriageOutcome: function (request) {
    var responseMap = {
      'src/mocks/stu3/recordTriageOutcome/requests/ReturnToReferrerWithAdvice.json': 'stu3/recordTriageOutcome/responses/ReturnToReferrerWithAdvice.json',
      'src/mocks/stu3/recordTriageOutcome/requests/AcceptReferBookLater.json': 'stu3/recordTriageOutcome/responses/AcceptReferBookLater.json',
      'src/mocks/stu3/recordTriageOutcome/requests/AttachmentIncluded.json': 'stu3/recordTriageOutcome/responses/AttachmentIncluded.json',
    }

    return mapExampleResponse(request, responseMap)


  },

  getResponseForAcceptReferral: function (request) {

    const ubrn = request.params.ubrn;

    if (ubrn === '000000070000') {
      return { responsePath: 'stu3/acceptReferral/responses/ExampleResponse.json', responseCode: 200 }
    }
    return {}

  },

  getResponseForCancelReferral: function (request) {
    var responseMap = {
      'src/mocks/stu3/cancelReferral/requests/IntendPrivateWithoutComment.json': 'stu3/cancelReferral/responses/CancelledReferralIntendPrivateWithoutComment.json',
      'src/mocks/stu3/cancelReferral/requests/PatientRequestCancellationOther.json': 'stu3/cancelReferral/responses/CancelledReferralPatientOther.json',
      'src/mocks/stu3/cancelReferral/requests/RaisedInError.json': 'stu3/cancelReferral/responses/CancelledReferralRaisedInError.json',
      'src/mocks/stu3/cancelReferral/requests/ReferrerCancellation.json': 'stu3/cancelReferral/responses/CancelledBookedReferralReferrerCancellation.json',
      'src/mocks/stu3/cancelReferral/requests/NoLongerRequired.json': 'stu3/cancelReferral/responses/CancelledReferralWithCancelledBookingNoLongerRequired.json',
      'src/mocks/stu3/cancelReferral/requests/IntendPrivateWithComment.json': 'stu3/cancelReferral/responses/CancelledReferralResolvedDeferralIntendPrivateWithComment.json'
    }

    return mapExampleResponse(request, responseMap)
  },

  getResponseForRejectReferral: function (request) {
    var responseMap = {
      'src/mocks/stu3/rejectReferral/requests/BasicExampleIbs.json': 'stu3/rejectReferral/responses/ExampleResponseIbs.json',
      'src/mocks/stu3/rejectReferral/requests/BasicExampleDbs.json': 'stu3/rejectReferral/responses/ExampleResponseDbs.json'
    }

    return mapExampleResponse(request, responseMap)
  },

  getResponseForAvailableActionsForUserList: function (request) {

    const focus = request.query['focus']
    const intent = request.query['intent']
    const status = request.query['status']

    // Scenario 1 No "action" is available - A empty list is returned to the caller indicating there are no "actions" available currently
    if (focus === 'ReferralRequest/000000070000/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'stu3/availableActionsForUserList/Empty.json'
    }

    // Scenario 2 An "action" is available - Illustrate success response to caller
    if (focus === 'ReferralRequest/000000070001/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'stu3/availableActionsForUserList/WithRecordReviewOutcome.json'
    }

    if (focus === 'ReferralRequest/000000070002/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'stu3/availableActionsForUserList/WithCreateAppointment.json'
    }

    if (focus === 'ReferralRequest/000000070003/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'stu3/availableActionsForUserList/WithChangeShortlist.json'
    }

    if (focus === 'ReferralRequest/000000070004/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'stu3/availableActionsForUserList/WithChangeShortlistAndSendForTriage.json'
    }

    if (focus === 'ReferralRequest/000000070005/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'stu3/availableActionsForUserList/WithCancelReferral.json'
    }

    if (focus === 'ReferralRequest/000000070006/_history/6' && intent === 'proposal' && status === 'ready') {
      return 'stu3/availableActionsForUserList/WithCancelDBAppointment.json'
    }
  },

  getResponseForCancelAppointmentActionLater: function (request) {
    var responseMap = {
      'src/mocks/stu3/cancelAppointmentActionLater/requests/MinimalExampleDBS.json': 'stu3/cancelAppointmentActionLater/responses/MinimalExampleDBS.json',
      'src/mocks/stu3/cancelAppointmentActionLater/requests/PriorityChangeAndWithAttachmentsDBS.json': 'stu3/cancelAppointmentActionLater/responses/PriorityChangeAndWithAttachmentsDBS.json',
      'src/mocks/stu3/cancelAppointmentActionLater/requests/MinimalExampleIBS.json': 'stu3/cancelAppointmentActionLater/responses/MinimalExampleIBS.json',
    }

    return mapExampleResponse(request, responseMap)


  },

  getExampleResponseForChangeShortlist: function (request) {
    var responseMap = {
      'src/mocks/stu3/changeShortlist/requests/UnbookedReferral.json': 'stu3/changeShortlist/responses/UnbookedReferral.json',
      'src/mocks/stu3/changeShortlist/requests/UnbookedReferralMultipleServices.json': 'stu3/changeShortlist/responses/UnbookedReferralMultipleServices.json',
      'src/mocks/stu3/changeShortlist/requests/UnbookedReferralMixedShortlist.json': 'stu3/changeShortlist/responses/UnbookedReferralMixedShortlist.json'
    }

    return mapExampleResponse(request, responseMap)
  },

  getExampleResponseForChangeShortlistAndSendForTriage: function (request) {
      var responseMap = {
        'src/mocks/stu3/changeShortlistAndSendForTriage/requests/MinimalRequest.json': 'stu3/changeShortlistAndSendForTriage/responses/MinimalRequest.json'
      }

      return mapExampleResponse(request, responseMap)
  },

  getExampleResponseForRetrieveAppointment: function (request) {
      const id = request.params.id;
      const version = request.params.version

      // Scenario 1 - Booked to directly-bookable service
      if (id === '70000' && (version === undefined || version === '5')) {
        return { responsePath: 'stu3/retrieveAppointment/responses/BookedDBS.json', responseCode: 200 }
      }

      // Scenario 2 - Booked to indirectly-bookable service
      if (id === '70001' && (version === undefined || version === '5')) {
        return { responsePath: 'stu3/retrieveAppointment/responses/BookedIBS.json', responseCode: 200 }
      }

      // Scenario 3 - Appointment Deferral
      if (id === '70002' && (version === undefined || version === '5')) {
        return { responsePath: 'stu3/retrieveAppointment/responses/AppointmentDeferral.json', responseCode: 200 }
      }

      // Scenario 4 -	Triage Deferral
      if (id === '70003' && (version === undefined || version === '5')) {
        return { responsePath: 'stu3/retrieveAppointment/responses/TriageDeferral.json', responseCode: 200 }
      }

      // Scenario 5 -	Triage Response
      if (id === '70004' && (version === undefined || version === '5')) {
        return { responsePath: 'stu3/retrieveAppointment/responses/TriageResponse.json', responseCode: 200 }
      }

      // Scenario 6 -	Cancel Appointment Action Later
      if (id === '70005' && (version === undefined || version === '5')) {
        return { responsePath: 'stu3/retrieveAppointment/responses/CAAL.json', responseCode: 200 }
      }

      // Scenario 7 -	Cancelled
      if (id === '70006' && (version === undefined || version === '5')) {
        return { responsePath: 'stu3/retrieveAppointment/responses/Cancelled.json', responseCode: 200 }
      }

      // Scenario 8 -	Converted from A and G and Booked to DBS
      if (id === '70007' && (version === undefined || version === '5')) {
        return { responsePath: 'stu3/retrieveAppointment/responses/AandGConvertedToDBS.json', responseCode: 200 }
      }

      return {}
    },

  getExampleResponseForCreateAdvice: function (request) {
    const responseMap = {
      'src/mocks/stu3/createAdviceAndGuidance/requests/ExampleRCAWithAttachments.json': 'stu3/createAdviceAndGuidance/responses/ExampleRCAWithAttachments.json',
      'src/mocks/stu3/createAdviceAndGuidance/requests/ExampleRCWithoutAttachments.json': 'stu3/createAdviceAndGuidance/responses/ExampleRCWithoutAttachments.json'
    }

    return mapExampleResponse(request, responseMap)
  }
}
