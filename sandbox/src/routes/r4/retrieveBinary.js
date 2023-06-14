const businessFunctionValidator = require('../../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for retrieveBinary A039 (R4) endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/R4/Binary/{attachmentUuid}',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const uuid = request.params.attachmentUuid;
      const url = request.url.href;
      const objectStore = "/ObjectStore/RetrieveBinary/d497bbe3-f88b-45f1-b3d4-9c563e4c0f5f";
      const location = url.split('/FHIR')[0] + objectStore;

      if (uuid === '704c3791-0873-45e9-9a04-b51996f8d93f' && request.method === 'get') {
        const response = h.response().code(307)
        response.headers["Location"] = location;
        return response
      } else {
        return h.file('SandboxErrorOutcome.json').code(422);
      }

    }
  }
]
