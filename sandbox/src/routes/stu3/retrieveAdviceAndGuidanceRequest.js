const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

function retrieveAdviceAndGuidanceRequest(request, h) {
  const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

  const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
  if (validationResult) {
    return validationResult
  }

  const { responsePath } = mockResponseProvider.getResponseForRetrieveAdviceAndGuidanceRequest(request);
  if (responsePath != null) {
    return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json").etag("5", { weak: true })
  }

  return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422);
}

module.exports = [
  /**
   * Sandbox implementation for retrieveAdviceAndGuidanceRequest endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/STU3/CommunicationRequest/{ubrn}',
    handler: (request, h) => {
      return retrieveAdviceAndGuidanceRequest(request, h);
    }
  },
  {
    method: 'GET',
    path: '/FHIR/STU3/CommunicationRequest/{ubrn}/_history/{version}',
    handler: (request, h) => {
      return retrieveAdviceAndGuidanceRequest(request, h);
    }
  }
]
