const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for rejectReferral endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/ReferralRequest/{ubrn}/$ers.rejectReferral',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      var responsePath = mockResponseProvider.getResponseForRejectReferral(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json").etag("10", { weak: true })
      }


      return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422);


    }
  }
]
