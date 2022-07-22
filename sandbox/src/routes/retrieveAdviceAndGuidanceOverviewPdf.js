const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for retrieveAdviceAndGuidanceOverviewPdf endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/CommunicationRequest/{ubrn}/$ers.generateCRI',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      // Simply checking if ubrn is supplied
      if (request.params.ubrn) {

        const { responsePath, responseCode, filename } = mockResponseProvider.getExampleResponseForRetrieveAdviceAndGuidanceOverviewPdf();
        if (responsePath && responseCode) {
          return h.file(responsePath, {
            mode: 'attachment',
            filename: filename
          }).code(responseCode);
        }
      }

      return h.file('SandboxErrorOutcome.json').code(422);


    }
  }
]
