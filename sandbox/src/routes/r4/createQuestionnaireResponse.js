const mockResponseProvider = require('../../services/mockResponseProvider');

function createQuestionnaireResponse(request, h) {
    const responsePath = mockResponseProvider.getExampleResponseForCreateQuestionnaireResponse(request);
    if (responsePath) {
        return h.file(responsePath, { etagMethod: false }).code(201).type('application/fhir+json').etag('1', { weak: true })
    }
}

module.exports = [
    /**
     * Sandbox implementation for the R4 Create QuestionnaireResponse endpoint
     */
    {
        method: 'POST',
        path: '/FHIR/R4/QuestionnaireResponse',
        handler: (request, h) => {
            return createQuestionnaireResponse(request, h);
        }
    }
]