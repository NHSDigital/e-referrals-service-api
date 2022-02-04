const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for acceptReferral endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/ReferralRequest/{ubrn}/$ers.acceptReferral',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)

      if (validationResult) {
        return validationResult
      }

      const { responsePath } = mockResponseProvider.getResponseForAcceptReferral(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json").etag("9", { weak: true })
      }

      return h.file('SandboxErrorOutcome.json').code(422);
    }
  }
]
