const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for bookOrDeferAppointment endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/Appointment',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      var responsePath = mockResponseProvider.getExampleResponseForBookOrDeferAppointment(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(201).type("application/fhir+json").etag("1", { weak: true })
      }


      return h.file('SandboxErrorOutcome.json').code(422);


    }
  }
]
