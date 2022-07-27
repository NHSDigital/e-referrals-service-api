const getStatus = require('./getStatus')
const getPing = require('./getPing')
const createReferral = require('./createReferral')
const createReferralAndSendForTriage = require('./createReferralAndSendForTriage')
const patientServiceSearch = require('./patientServiceSearch')
const getCodeSystem = require('./getCodeSystem')
const retrieveAppointmentSlots = require('./retrieveAppointmentSlots')
const retrieveBusinessFunctions = require('./r4/retrieveBusinessFunctions')
const retrieveOboUsers = require('./r4/retrieveOboUsers')
const uploadFileToDocumentStore = require('./uploadFileToDocumentStore')
const generatePatientLetter = require('./generatePatientLetter')
const retrieveAttachment = require('./retrieveAttachment')
const retrieveReferralRequest = require('./retrieveReferralRequest')
const maintainReferralLetter = require('./maintainReferralLetter')
const bookOrDeferAppointment = require('./bookOrDeferAppointment')
const updateAppointment = require('./updateAppointment')
const retrieveClinicalInformation = require('./retrieveClinicalInformation')
const retrieveWorklist = require('./retrieveWorklist')
const retrieveAdviceAndGuidanceWorklist = require('./retrieveAdviceAndGuidanceWorklist')
const retrieveHealthcareService = require('./r4/retrieveHealthcareService')
const searchForHealthcareServices = require('./r4/searchForHealthcareServices')
const retrieveAdviceAndGuidanceRequest = require('./retrieveAdviceAndGuidanceRequest')
const retrieveAdviceAndGuidanceConversation = require('./retrieveAdviceAndGuidanceConversation')
const sendAdviceAndGuidanceResponse = require('./sendAdviceAndGuidanceResponse')
const convertAdviceAndGuidanceToReferral = require('./convertAdviceAndGuidanceToReferral')
const recordTriageOutcome = require('./recordTriageOutcome')
const acceptReferral = require('./acceptReferral')
const rejectReferral = require('./rejectReferral')
const availableActionsForUserList = require('./availableActionsForUserList')
const cancelAppointmentActionLater = require('./cancelAppointmentActionLater')
const changeShortlist = require('./changeShortlist')
const changeShortlistAndSendForTriage = require('./changeShortlistAndSendForTriage')
const cancelReferral = require('./cancelReferral')
const retrieveAppointment = require('./retrieveAppointment')
const retrieveAdviceAndGuidanceOverviewPdf = require('./retrieveAdviceAndGuidanceOverviewPdf')

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
  retrieveAdviceAndGuidanceOverviewPdf
)

module.exports = routes
