const fs = require('fs')
const lodash = require('lodash')

function mapExampleResponse(request, exampleResponseMap) {

  if (request && request.payload) {
    for (const [requestBodyPath, response] of Object.entries(exampleResponseMap)) {
      try {
      console.error(fs.readFileSync(requestBodyPath, 'utf8'));
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

  getExampleResponseForPostServiceRequest: function (request) {
    var responseMap = {
      'src/mocks/r4/createServiceRequest/requests/createIncomplete.json': {responsePath: 'r4/createServiceRequest/responses/createdIncomplete.json', responseCode: 201}
    }
    return mapExampleResponse(request, responseMap)
  },

  getExampleResponseForPostDocumentReference: function (request) {
    var responseMap = {
      'src/mocks/r4/createDocumentReference/requests/AdviceRequestAttachment.json': {responsePath: 'r4/createDocumentReference/responses/AdviceRequestAttachment.json', responseCode: 201}
    }
    return mapExampleResponse(request, responseMap)
  },

  getExampleResponseForPostCommunication: function (request) {
    var responseMap = {
      'src/mocks/r4/sendCommunication/requests/initialCommunication.json': {responsePath: 'r4/sendCommunication/responses/initialCommunication.json', responseCode: 201}
    }
    return mapExampleResponse(request, responseMap)
  },
  getExampleResponseForPostQuestionnaireResponse: function (request) {
    var responseMap = {
      'src/mocks/r4/sendQuestionnaireResponse/requests/basicQuestionnaireResponse.json': {responsePath: 'r4/sendQuestionnaireResponse/responses/basicQuestionnaireResponse.json', responseCode: 201}
    }
    return mapExampleResponse(request, responseMap)
  },

  getExampleResponseForGetServiceRequest: function (request) {
    const version = request.params.version
    const uuid = request.params.uuid

    if (uuid == 1 && (!version || version == 1)) {
      return 'r4/getServiceRequest/responses/adviceRequestedAandG.json'
    }

    if (uuid == 2 && (!version || version == 1)) {
      return 'r4/getServiceRequest/responses/incompleteAandG.json'
    }

    if (uuid == 3 && (!version || version == 1)) {
      return 'r4/getServiceRequest/responses/shortlistedAandG.json'
    }

    if (uuid == 4 && (!version || version == 1)) {
      return 'r4/getServiceRequest/responses/shortlistedAandGAttachment.json'
    }

    return null
  },

  getExampleResponseForGetCommunication: function (request) {
    const version = request.params.version
    const uuid = request.params.uuid

    if (uuid == 1 && (!version || version == 1)) {
      return 'r4/getCommunication/responses/initialCommunication.json'
    }

    return null
  },

  getExampleResponseForGetDocumentReference: function (request) {
    const version = request.params.version
    const uuid = request.params.uuid

    if (uuid == 1 && (!version || version == 1)) {
      return 'r4/getDocumentReference/responses/AdviceRequestAttachment.json'
    }

    return null
  },

  getExampleResponseForGetQuestionnaireResponse: function (request) {
    const version = request.params.version
    const uuid = request.params.uuid

    if (uuid == 1 && (!version || version == 1)) {
      return 'r4/getQuestionnaireResponse/responses/basicQuestionnaireResponse.json'
    }

    return null
  },
}
