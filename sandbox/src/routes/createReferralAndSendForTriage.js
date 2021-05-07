const mockResponseProvider = require('../services/mockResponseProvider')

module.exports = [
  /**
   * Sandbox implementation for createReferralAndSendForTriage endpoint
   */
  {
    method: 'POST',
    path: '/STU3/v1/ReferralRequest/$ers.createReferralAndSendForTriage',
    handler: (request, h) => {

      var responsePath = mockResponseProvider.getExampleResponseForCreateReferralAndSendForTriage(request);
      if (responsePath != null) {
        return h.file(responsePath).code(201)
      } else {
        return h.file('GenericOperationOutcome.json').code(422);
      }

    }
  }
]
