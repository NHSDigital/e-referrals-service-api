const getStatus = require('./getStatus')
const getHealth = require('./getHealth')
const getPing = require('./getPing')
const createReferral = require('./createReferral')
const createReferralAndSendForTriage = require('./createReferralAndSendForTriage')
const patientServiceSearch = require('./patientServiceSearch')
const getCodeSystem = require('./getCodeSystem')
const retrieveAppointmentSlots = require('./retrieveAppointmentSlots')
const retrieveBusinessFunctions = require('./retrieveBusinessFunctions')
const uploadFileToDocumentStore = require('./uploadFileToDocumentStore')
const generatePatientLetter = require('./generatePatientLetter')
const retrieveAttachment = require('./retrieveAttachment')
const retrieveReferralRequest = require('./retrieveReferralRequest')
const maintainReferralLetter = require('./maintainReferralLetter')
const bookOrDeferAppointment = require('./bookOrDeferAppointment')
const retrieveClinicalInformation = require('./retrieveClinicalInformation')
const retrieveWorklist = require('./retrieveWorklist')
const retrieveAdviceAndGuidanceWorklist = require('./retrieveAdviceAndGuidanceWorklist')
const retrieveHealthcareService = require('./retrieveHealthcareService')
const searchForHealthcareServices = require('./searchForHealthcareServices')
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

const routes = [].concat(
  getStatus,
  getHealth,
  getPing,
  createReferral,
  createReferralAndSendForTriage,
  patientServiceSearch,
  getCodeSystem,
  retrieveAppointmentSlots,
  retrieveBusinessFunctions,
  uploadFileToDocumentStore,
  generatePatientLetter,
  retrieveAttachment,
  retrieveReferralRequest,
  maintainReferralLetter,
  bookOrDeferAppointment,
  retrieveClinicalInformation,
  retrieveWorklist,
  retrieveAdviceAndGuidanceWorklist,
  retrieveHealthcareService,
  searchForHealthcareServices,
  changeShortlist,
  retrieveAdviceAndGuidanceRequest,
  retrieveAdviceAndGuidanceConversation,
  sendAdviceAndGuidanceResponse,
  convertAdviceAndGuidanceToReferral,
  recordTriageOutcome,
  acceptReferral,
  rejectReferral,
  availableActionsForUserList,
  cancelAppointmentActionLater,
  retrieveHealthcareService,
  searchForHealthcareServices,
  changeShortlist,
  changeShortlistAndSendForTriage
)

module.exports = routes
