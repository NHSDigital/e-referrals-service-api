const mockResponseProvider = require('../services/mockResponseProvider');
const businessFunctionValidator = require('../services/businessFunctionValidator');

module.exports = [
  /**
     * Sandbox implementation for getCodeSystem endpoint
     */
  {
    method: 'GET',
    path: '/STU3/v1/CodeSystem/{codeSystemType}',
    handler: (request, h) => {
        
      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN"];
      
      if (!businessFunctionValidator.hasValidBusinessFunction(request, allowedBusinessFunctions)) {
        return h.response('This endpoint cannot be accessed using business role provided').code(403);
      }

      var responsePath = mockResponseProvider.getExampleResponseForGetCodeSystem(request.params.codeSystemType);
      if (responsePath != null) {
        return h.file(responsePath).code(200).type("application/fhir+json");
      } 
        
      return h.response().code(404);
      
    }
  }
]
