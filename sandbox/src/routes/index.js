/**
 * FHIR STU3 Version
 */
const getStatus = require('./stu3/getStatus')
const getPing = require('./stu3/getPing')
const createReferral = require('./stu3/createReferral')
const createReferralAndSendForTriage = require('./stu3/createReferralAndSendForTriage')
const patientServiceSearch = require('./stu3/patientServiceSearch')
const getCodeSystem = require('./stu3/getCodeSystem')
const retrieveAppointmentSlots = require('./stu3/retrieveAppointmentSlots')
const uploadFileToDocumentStore = require('./stu3/uploadFileToDocumentStore')
const generatePatientLetter = require('./stu3/generatePatientLetter')
const retrieveAttachment = require('./stu3/retrieveAttachment')
const retrieveReferralRequest = require('./stu3/retrieveReferralRequest')
const maintainReferralLetter = require('./stu3/maintainReferralLetter')
const bookOrDeferAppointment = require('./stu3/bookOrDeferAppointment')
const updateAppointment = require('./stu3/updateAppointment')
const retrieveClinicalInformation = require('./stu3/retrieveClinicalInformation')
const retrieveWorklist = require('./stu3/retrieveWorklist')
const retrieveAdviceAndGuidanceWorklist = require('./stu3/retrieveAdviceAndGuidanceWorklist')
const retrieveAdviceAndGuidanceRequest = require('./stu3/retrieveAdviceAndGuidanceRequest')
const retrieveAdviceAndGuidanceConversation = require('./stu3/retrieveAdviceAndGuidanceConversation')
const sendAdviceAndGuidanceResponse = require('./stu3/sendAdviceAndGuidanceResponse')
const convertAdviceAndGuidanceToReferral = require('./stu3/convertAdviceAndGuidanceToReferral')
const recordTriageOutcome = require('./stu3/recordTriageOutcome')
const acceptReferral = require('./stu3/acceptReferral')
const rejectReferral = require('./stu3/rejectReferral')
const availableActionsForUserList = require('./stu3/availableActionsForUserList')
const cancelAppointmentActionLater = require('./stu3/cancelAppointmentActionLater')
const changeShortlist = require('./stu3/changeShortlist')
const changeShortlistAndSendForTriage = require('./stu3/changeShortlistAndSendForTriage')
const cancelReferral = require('./stu3/cancelReferral')
const retrieveAppointment = require('./stu3/retrieveAppointment')
const retrieveAdviceAndGuidanceOverviewPdf = require('./stu3/retrieveAdviceAndGuidanceOverviewPdf')
const createAdviceAndGuidance = require('./stu3/createAdviceAndGuidanceRequest')

/**
 * FHIR R4 Version
 */
const retrieveBusinessFunctions = require('./r4/retrieveBusinessFunctions')
const retrieveOboUsers = require('./r4/retrieveOboUsers')
const retrieveHealthcareService = require('./r4/retrieveHealthcareService')
const searchForHealthcareServices = require('./r4/searchForHealthcareServices')
const searchServiceRequest = require('./r4/searchServiceRequest')

const routes = [].concat(
  getStatus,
  getPing,
  createReferral,
  createReferralAndSendForTriage,
  patientServiceSearch,
  getCodeSystem,
  retrieveAppointmentSlots,
  retrieveBusinessFunctions,
  retrieveOboUsers,
  uploadFileToDocumentStore,
  generatePatientLetter,
  retrieveAttachment,
  retrieveReferralRequest,
  maintainReferralLetter,
  bookOrDeferAppointment,
  updateAppointment,
  retrieveClinicalInformation,
  retrieveWorklist,
  retrieveAdviceAndGuidanceWorklist,
  retrieveHealthcareService,
  searchForHealthcareServices,
  changeShortlist,
  changeShortlistAndSendForTriage,
  retrieveAdviceAndGuidanceRequest,
  retrieveAdviceAndGuidanceConversation,
  sendAdviceAndGuidanceResponse,
  convertAdviceAndGuidanceToReferral,
  recordTriageOutcome,
  acceptReferral,
  rejectReferral,
  availableActionsForUserList,
  cancelAppointmentActionLater,
  cancelReferral,
  retrieveAppointment,
  retrieveAdviceAndGuidanceOverviewPdf,
  searchServiceRequest,
  createAdviceAndGuidance
)

module.exports = routes
