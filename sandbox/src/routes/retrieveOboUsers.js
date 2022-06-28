const mockResponseProvider = require('../services/mockResponseProvider')

module.exports = [
    /**
     * Sandbox implementation for retrieveOboUsers endpoint
     */
    {
        method: 'GET',
        path: '/FHIR/R4/Practitioner',
        handler: (request, h) => {
            
            // check that the query exists and is correct
            const query = request.query._query;
            if (query == undefined || query != "onBehalfOf") {
                return h.file('SandboxErrorOutcome.json').code(400);
            }
            
            if (request.headers["nhsd-ers-business-function"] !== "SERVICE_PROVIDER_CLINICIAN_ADMIN")
            {
                return h.response("This endpoint can only be accessed with the SERVICE_PROVIDER_CLINICIAN_ADMIN business function").code(403);
            }

            const { responsePath, responseCode } = mockResponseProvider.getExampleResponseForRetrieveOboUsers();
            if (responsePath && responseCode) {
                return h.file(responsePath).code(responseCode).type("application/fhir+json");

            }

            // this should never happen as we always get a valid response for this endpoint
            return h.file('SandboxErrorOutcome.json').code(400);


        }
    }
]
