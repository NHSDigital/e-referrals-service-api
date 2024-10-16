const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

module.exports = [
  /**
   * Sandbox implementation for generatePatientLetter endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/ReferralRequest/{ubrn}/$ers.generatePatientLetter',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      // Simply checking if ubrn is supplied
      if (request.params.ubrn) {

        const { responsePath, responseCode, filename } = mockResponseProvider.getExampleResponseForGeneratePatientLetter();
        if (responsePath && responseCode) {
          return h.file(responsePath, {
            mode: 'attachment',
            filename: filename,
            etagMethod: false
          }).code(responseCode);
        }
      }

      return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422);


    }
  }
]
