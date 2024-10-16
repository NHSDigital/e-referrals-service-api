const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

module.exports = [
  /**
   * Sandbox implementation for Update Appointment endpoint
   */
  {
    method: 'PUT',
    path: '/FHIR/STU3/Appointment/{appointmentId}',
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

      const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const { responsePath, responseCode }  = mockResponseProvider.putExampleResponseForUpdateAppointment(request);
      if (responsePath != null) {
        return h.file(responsePath, { etagMethod: false }).code(responseCode).type("application/fhir+json").etag("5", { weak: true })
      }

      return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422);

    }
  }
]
