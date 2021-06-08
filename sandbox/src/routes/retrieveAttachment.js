const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for retrieveAttachment endpoint
   */
  {
    method: 'GET',
    path: '/STU3/v1/Binary/{attachmentLogicalID}',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const { responsePath, responseCode, filename } = mockResponseProvider.getExampleResponseForRetrieveAttachment(request);
      if (responsePath !== undefined && responseCode !== undefined) {
        return h.file(responsePath, {
          mode: 'attachment',
          filename: filename
        }).code(responseCode);
      }

      return h.file('SandboxErrorOutcome.json').code(422);
    }
  }
]
