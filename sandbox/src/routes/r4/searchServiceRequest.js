const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

function searchServiceRequest(request, h) {
    const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

    const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
    if (validationResult) {
        return validationResult
    }

    if(request.method == 'get') {
        var responsePath = mockResponseProvider.getExampleResponseForSearchServiceRequest(request)
        if (responsePath) {
            return h.file(responsePath, { etagMethod: false }).code(200).type('application/fhir+json')
        }
    }

    return h.file('r4/R4-SandboxErrorOutcome.json').code(400)
}


module.exports = [
    {
        method: 'GET',
        path: '/FHIR/R4/ServiceRequest',
        handler: searchServiceRequest
    }
]
