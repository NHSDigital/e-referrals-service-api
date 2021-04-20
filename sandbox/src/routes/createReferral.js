const requestValidator = require('../validators/request-validator')
const Boom = require('boom')

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

      if(!requestValidator.verifyContentTypeHeader(request, "application/fhir+json")){
	  	  const path = 'OperationErrorOutcome.json'
        return h.file(path).code(422)
      }
	  
      const requiredProperties = ["resourceType", "meta", "parameter"];
	    if(!requestValidator.verifyRequestHasProperties(request, requiredProperties)){
	  	  const path = 'OperationErrorOutcome.json'
        return h.file(path).code(422)
      }

      const path = 'ReferralRequest.json'
      return h.file(path)
    }
  }
]
