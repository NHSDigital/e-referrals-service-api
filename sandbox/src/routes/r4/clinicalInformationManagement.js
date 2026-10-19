const mockResponseProvider = require('./services/mockResponseProvider')
const clinicalInformationManagement = require('./services/clinicalInformationManagement')
const validationUtils = require('../common/validationUtils')

module.exports = [
  /**
   * Sandbox implementation for the FHIR R4 Clinical Information Management endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/R4',
    options: {
      payload: {
        failAction: (request, h) => {
          const { responseCode, body } = clinicalInformationManagement.malformedJsonResponse()
          return h.response(body).code(responseCode).type('application/fhir+json').takeover()
        }
      }
    },
    handler: (request, h) => {
      const allowedBusinessFunctions = [
        'SERVICE_PROVIDER_CLINICIAN',
        'SERVICE_PROVIDER_CLINICIAN_ADMIN'
      ]

      if (!request.headers['nhsd-ers-business-function']) {
        return h.response('SANDBOX_ERROR: This endpoint requires an e-RS Business Function header').code(403)
      }

      const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const { responseCode, body } = mockResponseProvider.getExampleResponseForClinicalInformationManagement(request)
      return h.response(body).code(responseCode).type('application/fhir+json')
    }
  }
]
