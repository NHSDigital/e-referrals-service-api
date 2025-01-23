const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

module.exports = [
  /**
   * Sandbox implementation for cancelReferral endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/ReferralRequest/{ubrn}/$ers.cancelReferral',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)

      if (validationResult) {
        return validationResult
      }

      const responsePath = mockResponseProvider.getResponseForCancelReferral(request);
      if (!responsePath) {
        return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422);
      }

      return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json")
    }
  }
]
