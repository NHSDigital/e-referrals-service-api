const mockResponseProvider = require('./services/mockResponseProvider')

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
                return h.file('r4/R4-SandboxErrorOutcome.json').code(400);
            }

            if (request.headers["nhsd-ers-business-function"] !== "SERVICE_PROVIDER_CLINICIAN_ADMIN")
            {
                return h.response('SANDBOX_ERROR: This endpoint cannot be accessed using the e-RS Business Function provided. Allowed values: SERVICE_PROVIDER_CLINICIAN_ADMIN').code(403)
            }

            const { responsePath, responseCode } = mockResponseProvider.getExampleResponseForRetrieveOboUsers();
            if (responsePath && responseCode) {
                return h.file(responsePath, { etagMethod: false }).code(responseCode).type("application/fhir+json");

            }

            // this should never happen as we always get a valid response for this endpoint
            return h.file('r4/R4-SandboxErrorOutcome.json').code(400);


        }
    }
]
