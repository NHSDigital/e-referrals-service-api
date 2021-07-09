const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for generatePatientLetter endpoint
   */
  {
    method: 'POST',
    path: '/STU3/v1/ReferralRequest/{ubrn}/$ers.generatePatientLetter',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      // Simply checking if ubrn is supplied
      if (request.params.ubrn) {

        const { responsePath, responseCode, filename } = mockResponseProvider.getExampleResponseForGeneratePatientLetter();
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
