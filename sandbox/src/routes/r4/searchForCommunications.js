const mockResponseProvider = require('../../services/mockResponseProvider');

function searchForCommunications(request, h) {
    const responsePath = mockResponseProvider.getExampleResponseForSearchForCommunication(request);
    if (responsePath) {
        return h.file(responsePath, { etagFunction: false }).code(200).type('application/fhir+json');
    }

    return h.file('SandboxErrorOutcome.json').code(400);
}

module.exports = [
    /**
     * Sandbox implementation for the Search for Communications endpoint.
     */
    {
        method: 'GET',
        path: '/FHIR/R4/Communication',
        handler: (request, h) => {
            return searchForCommunications(request, h);
        }
    }
]