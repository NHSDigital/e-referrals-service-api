const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

function retrieveAdviceAndGuidanceConversation(request, h) {
  const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

  const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
  if (validationResult) {
    return validationResult
  }

  const { responsePath, version } = mockResponseProvider.getResponseForRetrieveAdviceAndGuidanceConversation(request);
  if (responsePath != null) {
    return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json").etag(version, { weak: true })
  }

  return h.file('stu3/STU3-SandboxErrorOutcome.json').code(400);
}

module.exports = [
  /**
   * Sandbox implementation for retrieveAdviceAndGuidanceConversation endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/STU3/Communication',
    handler: (request, h) => {
      return retrieveAdviceAndGuidanceConversation(request, h);
    }
  }
]
