const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

module.exports = [
  /**
   * Sandbox implementation for uploadFileToDocumentStore A039 (R4) endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/R4/Binary',
    handler: (request, h) => {
      const allowedBusinessFunctions = ['REFERRING_CLINICIAN', 'REFERRING_CLINICIAN_ADMIN', 'SERVICE_PROVIDER_CLINICIAN', 'SERVICE_PROVIDER_CLINICIAN_ADMIN']

      const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const exampleResponse = mockResponseProvider.getExampleResponseForUploadFileToDocumentStore(request)
      if (exampleResponse) {
        const { responsePath, responseCode, location, contentDisposition } = exampleResponse
        return h.file(responsePath, { etagMethod: false })
          .code(responseCode)
          .type('application/fhir+json')
          .header('Location', location)
          .header('Content-Disposition', contentDisposition)
      }

      return h.file('r4/uploadFileToDocumentStore/responses/OperationOutcome-422.json').code(422).type('application/fhir+json')
    }
  }
]

