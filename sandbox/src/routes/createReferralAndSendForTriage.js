const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for createReferralAndSendForTriage endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/ReferralRequest/$ers.createReferralAndSendForTriage',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      var responsePath = mockResponseProvider.getExampleResponseForCreateReferralAndSendForTriage(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(201).type("application/fhir+json").etag("1", { weak: true })
      } else {
        return h.file('SandboxErrorOutcome.json').code(422);
      }

    }
  }
]
