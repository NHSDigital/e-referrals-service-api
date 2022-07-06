const mockResponseProvider = require('../../services/mockResponseProvider');

function getServiceRequest(request, h) {
    const responseDetails = mockResponseProvider.getExampleResponseForGetServiceRequest(request);
    if (responseDetails) {
        return h.file(responseDetails.path, { etagMethod: false }).code(200).type("application/fhir+json").etag(responseDetails.version, { weak: true });
    }

    return h.file('SandboxErrorOutcome.json').code(404);
}

module.exports = [
    /**
     * Sandbox implementation of the Get ServiceRequest endpoint.
     */
    {
        method: 'GET',
        path: '/FHIR/R4/ServiceRequest/{id}',
        handler: (request, h) => {
            return getServiceRequest(request, h);
        }
    },
    {
        method: 'GET',
        path: '/FHIR/R4/ServiceRequest/{id}/_history/{version}',
        handler: (request, h) => {
            return getServiceRequest(request, h);
        }
    }
]