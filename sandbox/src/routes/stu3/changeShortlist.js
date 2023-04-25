const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

module.exports = [
    /**
     * Sandbox implementation for the changeShortlist Endpoint
     */
    {
        method: 'POST',
        path: '/FHIR/STU3/ReferralRequest/{ubrn}/$ers.changeShortlist',
        handler: (request, h) => {
            const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]
            const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)

            if (validationResult) {
                return validationResult
            }

            const responsePath = mockResponseProvider.getExampleResponseForChangeShortlist(request);
            if (!responsePath) {
                return h.file('STU3-SandboxErrorOutcome.json').code(422)
            }

            return h.file(responsePath, { etagMethod: false }).code(200).type('application/fhir+json').etag("3", { weak: true })
        }
    }
]