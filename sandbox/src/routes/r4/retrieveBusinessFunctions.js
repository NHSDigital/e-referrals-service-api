const mockResponseProvider = require('./services/mockResponseProvider')

module.exports = [
  /**
   * Sandbox implementation for retrieveBusinessFunctions endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/R4/PractitionerRole',
    handler: (request, h) => {

      const { responsePath, responseCode } = mockResponseProvider.getExampleResponseForRetrieveBusinessFunctions();
      if (responsePath && responseCode) {
        return h.file(responsePath, { etagMethod: false }).code(responseCode).type("application/fhir+json");

      }

      // this should never happen as we always get a valid response for this endpoint
      return h.file('./r4/R4-SandboxErrorOutcome.json').code(400);


    }
  }
]
