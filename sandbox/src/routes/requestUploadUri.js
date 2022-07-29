const mockResponseProvider = require('../services/mockResponseProvider')
const businessFunctionValidator = require('../services/businessFunctionValidator')

function requestUploadUri(request, h) {
    const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

    const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
    if (validationResult) {
        return validationResult
    }

    if(request.method == 'post') {
        var responsePath = mockResponseProvider.getExampleResponseForRequestUploadUri(request)
        if (responsePath) {
            return h.file(responsePath, { etagMethod: false }).code(200).type('application/fhir+json')
        }
    }

    return h.file('SandboxErrorOutcome.json').code(422)
}


module.exports = [
    {
        method: 'POST',
        path: '/FHIR/R4/ServiceRequest/{id}/$ers.generateUploadURI',
        handler: requestUploadUri
    }
]
