const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

function retrieveAppointment(request, h) {
  const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

  const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
  if (validationResult) {
    return validationResult
  }

  const { responsePath } = mockResponseProvider.getExampleResponseForRetrieveAppointment(request);
  if (responsePath != null) {
    return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json").etag("5", { weak: true })
  }

  return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422);
}

module.exports = [
  /**
   * Sandbox implementation for retrieveAppointment endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/STU3/Appointment/{id}',
    handler: (request, h) => {
      return retrieveAppointment(request, h);
    }
  },
  {
    method: 'GET',
    path: '/FHIR/STU3/Appointment/{id}/_history/{version}',
    handler: (request, h) => {
      return retrieveAppointment(request, h);
    }
  }
]
