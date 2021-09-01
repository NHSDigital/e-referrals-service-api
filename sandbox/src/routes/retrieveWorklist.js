const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for retrieveWorklist endpoint
   */
  {
    method: 'POST',
    path: '/STU3/ReferralRequest/$ers.fetchworklist',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN", "SERVICE_PROVIDER_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      var responsePath = mockResponseProvider.getExampleResponseForRetrieveWorklist(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json")
      }


      return h.file('SandboxErrorOutcome.json').code(422);


    }
  }
]
