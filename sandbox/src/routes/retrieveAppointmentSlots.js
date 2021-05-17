const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for retrieveAppointmentSlots endpoint
   */
  {
    method: 'GET',
    path: '/STU3/v1/Slot',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      if (!businessFunctionValidator.hasValidBusinessFunction(request, allowedBusinessFunctions)) {
        return h.response('SANDBOX_ERROR: This endpoint cannot be accessed using the e-RS Business Function provided. Allowed values: ' + allowedBusinessFunctions).code(403);
      }

      const { responsePath, responseCode } = mockResponseProvider.getExampleResponseForRetrieveAppointmentSlots(request);
      if (responsePath !== undefined && responseCode !== undefined) {
        return h.file(responsePath).code(responseCode).type("application/fhir+json");

      }


      return h.file('SandboxErrorOutcome.json').code(400);


    }
  }
]
