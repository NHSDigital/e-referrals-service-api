const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

module.exports = [
  /**
   * Sandbox implementation for retrieveWorklist endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/ReferralRequest/$ers.fetchworklist',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_ADMIN", "SERVICE_PROVIDER_CLINICIAN_ADMIN", "REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "REFERRING_ADMIN"]

      const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      var responsePath = mockResponseProvider.getExampleResponseForRetrieveWorklist(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json")
      }


      return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422);


    }
  }
]