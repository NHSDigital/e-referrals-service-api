const mockResponseProvider = require('./services/mockResponseProvider');
const businessFunctionValidator = require('../../services/businessFunctionValidator');

module.exports = [
  /**
   * Sandbox implementation for getCodeSystem endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/STU3/CodeSystem/{codeSystemType}',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"];

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      var responsePath = mockResponseProvider.getExampleResponseForGetCodeSystem(request.params.codeSystemType);
      if (responsePath != null) {
        return h.file(responsePath, {"etagMethod": false}).code(200).type("application/fhir+json");
      }

      return h.response().code(404);

    }
  }
]
