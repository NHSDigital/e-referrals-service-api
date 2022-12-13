const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for post ServiceRequest endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/R4/ServiceRequest',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const { responsePath, responseCode } = mockResponseProvider.getExampleResponseForPostServiceRequest(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(responseCode).type("application/fhir+json").etag("1", { weak: true })
      }

      return h.file('SandboxErrorOutcome.json').code(422);
    }
  }
]
