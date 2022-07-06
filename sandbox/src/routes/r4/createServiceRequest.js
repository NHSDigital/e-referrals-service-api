const mockResponseProvider = require('../../services/mockResponseProvider');

function createServiceRequest(request, h) {
    const responsePath = mockResponseProvider.getExampleResponseForCreateServiceRequest(request);
    if (responsePath) {
        return h.file(responsePath, { etagMethod: false }).code(201).type('application/fhir+json').etag('1', { weak: true });
    }

    return h.file('SandboxErrorOutcome.json').code(422);
}

module.exports = [
    /**
     * Sandbox implementation for the R4 Create ServiceRequest endpoint
     */
    {
        method: 'POST',
        path: '/FHIR/R4/ServiceRequest',
        handler: (request, h) => {
            return createServiceRequest(request, h);
        }
    }
]