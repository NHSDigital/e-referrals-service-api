const mockResponseProvider = require('../services/mockResponseProvider')

module.exports = [
  /**
   * Sandbox implementation for createReferral endpoint
   */
  {
    method: '*',
    path: '/STU3/v1/ReferralRequest/$ers.createReferral',
    handler: (request, h) => {
      if (request.raw.req.method !== 'POST') {
        const responseMessage = {
          error: `Request method must be POST, not ${request.raw.req.method}`
        } ;
        return h.response(responseMessage).code(405)
      }

      var responsePath = mockResponseProvider.getExampleResponseForCreateReferral(request);
      if(responsePath != null){
        return h.file(responsePath)
      }else{
        return h.file('GenericOperationErrorOutcome.json').code(422);
      }

    }
  }
]
