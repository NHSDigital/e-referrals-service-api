const mockResponseProvider = require('../../services/mockResponseProvider');

function getCommunication(request, h) {
    const path = mockResponseProvider.getExampleResponseForGetCommunication(request);

    if (path) {
        return h.file(path, {etagMethod: false}).code(200).type('application/fhir+json').etag('1', {weak: true});
    }

    return h.file('SandboxErrorOutcome.json').code(404);
}

module.exports = [
    /**
     * Sandbox implementation of the Get Communication endpoint.
     */
    {
        method: 'GET',
        path: '/FHIR/R4/Communication/{id}',
        handler: getCommunication
    },
    {
        method: 'GET',
        path: '/FHIR/R4/Communication/{id}/_history/{version}',
        handler: getCommunication
    }
]