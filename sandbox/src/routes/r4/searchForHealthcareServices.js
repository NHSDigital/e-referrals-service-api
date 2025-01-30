const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

module.exports = [
    {
        method: 'GET',
        path: '/FHIR/R4/HealthcareService',
        handler: (request, h) => {
            const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

            const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
            if (validationResult) {
                return validationResult
            }

            var responsePath = mockResponseProvider.getExampleResponseForSearchForHealthcareServices(request)
            if (responsePath) {
                return h.file(responsePath, { etagMethod: false }).code(200).type('application/fhir+json')
            }

            return h.file('NotFoundOutcome.txt').code(404)
        }
    }
]