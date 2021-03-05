module.exports = [
    /**
     * POST to /v1/STU3/ReferralRequest/$ers.createReferral
     * Return createReferralRequest.json back to the client 
     */
    {
        method: '*',
        path: '/v1/STU3/ReferralRequest/$ers.createReferral',
        handler: (request, h) => {
            if (request.raw.req.method !== 'POST') {
                const responseMessage = {
                    error: `Request method must be POST, not ${request.raw.req.method}`
                }

                return h.response(responseMessage).code(405)
            }

            const path = 'createReferralRequest.json'
            return h.file(path)
        }
    }
]