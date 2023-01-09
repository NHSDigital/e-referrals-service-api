const mockResponseProvider = require('./services/mockResponseProvider')
const businessFunctionValidator = require('../../services/businessFunctionValidator')

function retrieveCommunication(request, h) {
    const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

    const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
    if (validationResult) {
        return validationResult
    }

    if(request.method == 'HEAD') {
        if(request.params.uuid == 1) {
            return h.response(' ').code(200).type('application/fhir+json').etag('1', { weak: true }).removeHeader('content-length')
        }
    }
    else {
        var responsePath = mockResponseProvider.getExampleResponseForGetCommunication(request)
        if (responsePath) {
            return h.file(responsePath, { etagMethod: false }).code(200).type('application/fhir+json').etag('1', { weak: true })
        }
    }

    return h.file('../NotFoundOutcome.txt').code(404)
}


module.exports = [
    {
        method: 'GET',
        path: '/FHIR/R4/Communication/{uuid}',
        handler: retrieveCommunication
    }
]
