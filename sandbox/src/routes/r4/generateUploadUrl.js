const mockResponseProvider = require('../../services/mockResponseProvider');

function generateUploadUrl(request, h) {
    const responsePath = mockResponseProvider.getExampleResponseForGeneratePresignedUrl(request);
    if (responsePath) {
        return h.file(responsePath, { etagMethod: false }).code(201).type('application/fhir+json');
    }

    return h.file('SandboxErrorOutcome.json').code(404);
}

module.exports = [
    /**
     * Sandbox implementation of the Generate Upload URL endpoint.
     */
    {
        method: "POST",
        path: "/FHIR/R4/DocumentReference/{id}/$ers.generateUploadUrl",
        handler: (request, h) => {
            return generateUploadUrl(request, h);
        }
    }
]