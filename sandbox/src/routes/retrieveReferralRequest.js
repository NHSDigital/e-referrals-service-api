const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

function retrieveReferralRequest(request, h) {
  const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN"]

  const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
  if (validationResult) {
    return validationResult
  }

  const { responsePath } = mockResponseProvider.getExampleResponseForRetrieveReferralRequest(request);
  if (responsePath != null) {
    return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json").etag("5", { weak: true })
  }

  return h.file('SandboxErrorOutcome.json').code(422);
}

module.exports = [
  /**
   * Sandbox implementation for retrieveReferralRequest endpoint
   */
  {
    method: 'GET',
    path: '/STU3/v1/ReferralRequest/{ubrn}',
    handler: (request, h) => {
      return retrieveReferralRequest(request, h);
    }
  },
  {
    method: 'GET',
    path: '/STU3/v1/ReferralRequest/{ubrn}/_history/{version}',
    handler: (request, h) => {
      return retrieveReferralRequest(request, h);
    }
  }
]
