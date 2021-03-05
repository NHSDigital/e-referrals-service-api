module.exports = [
    /**
     * GET to /echoHeaders
     * Just return the headers supplied to the app for testing
     */
    {
        method: '*',
        path: '/echoHeaders',
        handler: (request, h) => {
            return h.response(JSON.stringify(request.headers)).code(200)
        }
    }
]