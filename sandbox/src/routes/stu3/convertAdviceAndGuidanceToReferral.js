const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for convertAdviceAndGuidanceToReferral endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/ReferralRequest/$ers.createFromCommunicationRequestActionLater',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      var responsePath = mockResponseProvider.getResponseForConvertAdviceAndGuidanceToReferral(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(201).type("application/fhir+json")
      }


      return h.file('SandboxErrorOutcome.json').code(422);


    }
  }
]
