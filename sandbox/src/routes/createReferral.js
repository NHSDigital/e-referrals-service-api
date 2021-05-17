const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for createReferral endpoint
   */
  {
    method: 'POST',
    path: '/STU3/v1/ReferralRequest/$ers.createReferral',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      if (!businessFunctionValidator.hasValidBusinessFunction(request, allowedBusinessFunctions)) {
        return h.response('SANDBOX_ERROR: This endpoint cannot be accessed using the e-RS Business Function provided. Allowed values: ' + allowedBusinessFunctions).code(403);
      }

      var responsePath = mockResponseProvider.getExampleResponseForCreateReferral(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(201).type("application/fhir+json").etag("1", { weak: true })
      }


      return h.file('SandboxErrorOutcome.json').code(422);


    }
  }
]
