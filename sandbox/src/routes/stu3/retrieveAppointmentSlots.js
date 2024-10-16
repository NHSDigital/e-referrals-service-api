const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

module.exports = [
  /**
   * Sandbox implementation for retrieveAppointmentSlots endpoint
   */
  {
    method: 'GET',
    path: '/FHIR/STU3/Slot',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const { responsePath, responseCode } = mockResponseProvider.getExampleResponseForRetrieveAppointmentSlots(request);
      if (responsePath && responseCode) {
        return h.file(responsePath, { etagMethod: false }).code(responseCode).type("application/fhir+json");

      }


      return h.file('stu3/STU3-SandboxErrorOutcome.json').code(400);


    }
  }
]
