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
  }
}
