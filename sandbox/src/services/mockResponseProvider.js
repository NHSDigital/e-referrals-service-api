
const fs = require('fs')
const lodash = require('lodash')

function mapExampleResponse(request, exampleResponseMap) {

    if(request != null && request.payload != null){

        for (const [requestBodyPath, responseBodyPath] of Object.entries(exampleResponseMap)) {

            const exampleRequestBody = JSON.parse(fs.readFileSync(requestBodyPath))

            var requestBody = request.payload;
            if('object' != (typeof requestBody)){
                requestBody = JSON.parse(request.payload)
            }
            if(lodash.isEqual(requestBody, exampleRequestBody)){
                return responseBodyPath;
            }
        }

    }

    return null;
}

module.exports = {


    getExampleResponseForCreateReferral: function (request) {

        var exampleResponseMap = { 
            'src/mocks/CreateReferralParameters.json': 'ReferralRequest.json', 
            'src/mocks/CreateReferralParametersTwentyServices.json': 'ReferralRequestTwentyServices.json'
         };

        return mapExampleResponse(request, exampleResponseMap);
        
    }


    
}
