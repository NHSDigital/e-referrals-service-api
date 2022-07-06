const mockResponseProvider = require('../../services/mockResponseProvider');

function createCommunication(request, h) {
    const responsePath = mockResponseProvider.getExampleResponseForCreateCommunication(request);
    if (responsePath) {
        return h.file(responsePath, { etagMethod: false }).code(201).type('application/fhir+json').etag('1', { weak: true });
    }

    return h.file('SandboxErrorOutcome.json').code(422);
}

module.exports = [
    /**
     * Sandbox implementation of the Create Communication endpoint
     */
    {
        method: "POST",
        path: "/FHIR/R4/Communication",
        handler: (request, h) => {
            return createCommunication(request, h);
        }
    }
]