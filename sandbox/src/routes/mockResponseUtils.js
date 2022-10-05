const fs = require('fs')
const lodash = require('lodash')

module.exports = {
    mapExampleResponse(request, exampleResponseMap) {

        if (request && request.payload) {
            for (const [requestBodyPath, response] of Object.entries(exampleResponseMap)) {
                try {
                    const exampleRequestBody = JSON.parse(fs.readFileSync(requestBodyPath))
                    var requestBody = request.payload;

                    if ('object' != (typeof requestBody)) {
                        requestBody = JSON.parse(request.payload)
                    }

                    if (lodash.isEqual(requestBody, exampleRequestBody)) {
                        return response;
                    }
                } catch (err) {
                    console.error(err)
                    throw err
                }
            }
        }

        return null;
    },

    mapExampleGetResponse(parameterValue, exampleResponseMap) {
        for (const [requestParameter, responseBodyPath] of Object.entries(exampleResponseMap)) {
            if (parameterValue === requestParameter) {
                return responseBodyPath;
            }
        }
    }
}
