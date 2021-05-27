const mockResponseProvider = require('../services/mockResponseProvider')

module.exports = [
  /**
   * Sandbox implementation for retrieveBusinessFunctions endpoint
   */
  {
    method: 'GET',
    path: '/R4/v1/PractitionerRole',
    handler: (request, h) => {

      const { responsePath, responseCode } = mockResponseProvider.getExampleResponseForRetrieveBusinessFunctions();
      if (responsePath !== undefined && responseCode !== undefined) {
        return h.file(responsePath).code(responseCode).type("application/fhir+json");

      }

      // this should never happen as we always get a valid response for this endpoint
      return h.file('SandboxErrorOutcome.json').code(400);


    }
  }
]
