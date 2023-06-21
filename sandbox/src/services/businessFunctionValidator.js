
module.exports = {
  validateBusinessFunction: function (request, h, allowedBusinessFunctions) {
    const requestedBusinessFunction = request.headers["nhsd-ers-business-function"]
    const oboUserId = request.headers["nhsd-ers-on-behalf-of-user-id"]

    if (request && requestedBusinessFunction) {

      if (!allowedBusinessFunctions.includes(requestedBusinessFunction)) {
        return h.response('SANDBOX_ERROR: This endpoint cannot be accessed using the e-RS Business Function provided. Allowed values: ' + allowedBusinessFunctions).code(403)
      }

      if (requestedBusinessFunction === 'SERVICE_PROVIDER_CLINICIAN_ADMIN') {
        if (!oboUserId) {
          return h.response('SANDBOX_ERROR: When this endpoint is accessed using the e-RS SERVICE_PROVIDER_CLINICIAN_ADMIN Business Function then an On-Behalf-Of User ID must be provided').code(403)
.code(403)
        }
      }
      else {
        if (oboUserId) {
          return h.response('SANDBOX_ERROR: An On-Behalf-Of User ID must only be provided if this endpoint is accessed using the e-RS SERVICE_PROVIDER_CLINICIAN_ADMIN Business Function').code(403)
        }
      }
    }

    return undefined;
  }
}
