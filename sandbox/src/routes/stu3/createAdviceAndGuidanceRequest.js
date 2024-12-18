const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')
const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

module.exports = [
    /**
     * Sandbox implementation of the createAdvice endpoint
     */
  {
    method: 'POST',
    path: '/FHIR/STU3/CommunicationRequest/$ers.createAdviceAndGuidance',
    handler: (request, h) => {
      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const responsePath = mockResponseProvider.getExampleResponseForCreateAdvice(request)
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(200).type('application/fhir+json')
      }

      return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422)
    }
  }
]