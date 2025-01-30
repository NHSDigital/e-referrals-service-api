const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

function retrieveAvailableActionsForUserList(request, h) {
  const allowedBusinessFunctions = ["SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN", "REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

  const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
  if (validationResult) {
    return validationResult
  }

  const responsePath = mockResponseProvider.getResponseForAvailableActionsForUserList(request);
  if (responsePath) {
    return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json")
  }

  return h.file('stu3/STU3-SandboxErrorOutcome.json').code(400);
}

module.exports = [
  /**
   * Sandbox implementation for AvailableActionsForUserList endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/STU3/Task',
    handler: (request, h) => {
      return retrieveAvailableActionsForUserList(request, h);
    }
  }
]
