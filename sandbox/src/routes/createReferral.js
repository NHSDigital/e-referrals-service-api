const mockResponseProvider = require('../services/mockResponseProvider')

module.exports = [
  /**
   * Sandbox implementation for createReferral endpoint
   */
  {
    method: 'POST',
    path: '/STU3/v1/ReferralRequest/$ers.createReferral',
    handler: (request, h) => {

      var responsePath = mockResponseProvider.getExampleResponseForCreateReferral(request);
      if(responsePath != null){
        return h.file(responsePath).code(201)
      }else{
        return h.file('GenericOperationOutcome.json').code(422);
      }

    }
  }
]
