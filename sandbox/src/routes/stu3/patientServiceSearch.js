const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for searchHealthcareServicesForPatient endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/HealthcareService/$ers.searchHealthcareServicesForPatient',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      var responsePath = mockResponseProvider.getExampleResponseForPatientServiceSearch(request);

      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json")
      } else {
        return h.file('STU3-SandboxErrorOutcome.json').code(422);
      }

    }
  }
]
