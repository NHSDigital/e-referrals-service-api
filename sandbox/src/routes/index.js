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
  retrieveAdviceAndGuidanceWorklist
)

module.exports = routes
