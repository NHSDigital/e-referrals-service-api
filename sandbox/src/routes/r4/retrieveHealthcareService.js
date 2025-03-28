const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

function retrieveHealthcareService(request, h) {
    const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN"]

    const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
    if (validationResult) {
        return validationResult
    }

    if(request.method == 'HEAD') {
        if(request.params.serviceId == 1) {
            return h.response(' ').code(200).type('application/fhir+json').etag('1', { weak: true }).removeHeader('content-length')
        }
    }
    else {
        var responsePath = mockResponseProvider.getExampleResponseForGetHealthcareService(request)
        if (responsePath) {
            return h.file(responsePath, { etagMethod: false }).code(200).type('application/fhir+json').etag('1', { weak: true })
        }
    }

    return h.file('NotFoundOutcome.txt').code(404)
}


module.exports = [
    {
        method: 'GET',
        path: '/FHIR/R4/HealthcareService/{serviceId}',
        handler: retrieveHealthcareService
    }
]
