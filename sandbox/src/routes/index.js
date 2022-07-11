const getStatus = require('./getStatus')
const getPing = require('./getPing')
const createReferral = require('./createReferral')
const createReferralAndSendForTriage = require('./createReferralAndSendForTriage')
const patientServiceSearch = require('./patientServiceSearch')
const getCodeSystem = require('./getCodeSystem')
const retrieveAppointmentSlots = require('./retrieveAppointmentSlots')
const retrieveBusinessFunctions = require('./retrieveBusinessFunctions')
const retrieveOboUsers = require('./retrieveOboUsers')
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
const cancelReferral = require('./cancelReferral')
const retrieveAppointment = require('./retrieveAppointment')
const createServiceRequest = require('./r4/createServiceRequest')
const createQuestionnaireResponse = require('./r4/createQuestionnaireResponse')
const getServiceRequest = require('./r4/getServiceRequest')
const createCommunication = require('./r4/createCommunication')
const createDocumentReference = require('./r4/createDocumentReference')
const searchForCommunications = require('./r4/searchForCommunications')
const getCommunication = require('./r4/getCommunication')

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
  createServiceRequest,
  createQuestionnaireResponse,
  getServiceRequest,
  createCommunication,
  createDocumentReference,
  searchForCommunications,
  getCommunication
)

module.exports = routes
