const businessFunctionValidator = require('../../services/businessFunctionValidator')
const validationUtil = require('../common/validationUtil')

module.exports = [
  /**
   * Sandbox implementation for Retrieve attachment A042 (R4) endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/R4/Binary/{binaryId}',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"];

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions);
      if (validationResult) {
        return validationResult;
      }

      const binaryId = request.params.binaryId;
      const url = request.url.href;
      const objectStore = "/ObjectStore/d497bbe3-f88b-45f1-b3d4-9c563e4c0f5f";
      const location = url.split('/FHIR')[0] + objectStore;

      if ((validationUtil.hasLegacyPrefix(binaryId) || validationUtil.isValidUuid(binaryId)) && request.method === 'get') {
        const response = h.response().code(307);
        response.headers["Location"] = location;
        return response;
      } else {
        return h.file('r4/R4-SandboxErrorOutcome.json').code(400);
      }

    }
  }
]
