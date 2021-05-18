const mockResponseProvider = require('../services/mockResponseProvider')

module.exports = [
  /**
   * Sandbox implementation for searchHealthcareServicesForPatient endpoint
   */
  {
    method: 'POST',
    path: '/STU3/v1/HealthcareService/$ers.searchHealthcareServicesForPatient',
    handler: (request, h) => {

      var responsePath = mockResponseProvider.getExampleResponseForPatientServiceSearch(request);
      if (responsePath != null) {
        return h.file(responsePath).code(200)
      } else {
        return h.file('SandboxErrorOutcome.json').code(422);
      }

    }
  }
]
