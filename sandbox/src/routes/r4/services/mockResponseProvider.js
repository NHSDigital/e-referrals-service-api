const fs = require('fs')
const lodash = require('lodash')

function mapExampleResponse(request, exampleResponseMap) {

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
}


module.exports = {

  getExampleResponseForRetrieveBusinessFunctions: function () {

    return { responsePath: 'r4/retrieveBusinessFunctions/responses/PractitionerRoleBundle.json', responseCode: 200 }
  },

  getExampleResponseForRetrieveOboUsers: function () {
    return { responsePath: 'r4/retrieveOboUsers/responses/PractitionerBundle.json', responseCode: 200 }
  },

  getExampleResponseForGetHealthcareService: function (request) {
    const version = request.params.version
    const serviceId = request.params.serviceId

    if (serviceId == 1 && (!version || version == 1)) {
      return 'r4/getService/responses/sampleServiceWithMinimumAttributes.json'
    }

    if (serviceId == 2 && (!version || version == 1)) {
      return 'r4/getService/responses/sampleServiceWithFullAttributes.json'
    }

    return null
  },

  getExampleResponseForSearchForHealthcareServices: function (request) {
    const ids = request.query['_id']

    if (ids == ['1', '2']) {
      return 'r4/searchForServices/responses/searchServiceWithMinmumalAttributes.json'
    }

    if (ids == ['3', '4']) {
      return 'r4/searchForServices/responses/searchServiceWithMaxAndMinAttributes.json'
    }

    if (ids == ['5', '6']) {
      return 'r4/searchForServices/responses/searchServiceWithEmptyResponse.json'
    }

    return null
  },

  getExampleResponseForSearchServiceRequest: function (request) {
    let ubrn;
    const identifier = request.query.identifier;
    
    if (identifier.includes('|')) {
      ubrn = identifier.split('|')[1]
    }
    else {
      ubrn = identifier
    }

    if (ubrn === '000000070000') {
      return 'r4/searchServiceRequest/responses/ResponseExample.json'
    }

    return {}
  },

  getExampleResponseForRequestUploadUri: function (request) {
    const id = request.params.id
    if (id === 'r.f6dc823a-e673-4f74-9edc-a49525edd2a5') {
      var responseMap = {
        'src/mocks/r4/requestUploadUri/requests/RequestExample.json': 'r4/requestUploadUri/responses/ResponseExample.json'
      }
      return mapExampleResponse(request, responseMap)
    }
  }
}
