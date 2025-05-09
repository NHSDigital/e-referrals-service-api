/**
 * @file validationUtil.js
 * @description Provides utility functions.
 */

function isValidUuid(string) {
    return /^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i.test(string);
  }

function hasLegacyPrefix(string) {
    return string.startsWith('att-');
}

function validateBusinessFunction(request, h, allowedBusinessFunctions) {
    const requestedBusinessFunction = request.headers["nhsd-ers-business-function"]
    const oboUserId = request.headers["nhsd-ers-on-behalf-of-user-id"]

    if (request && requestedBusinessFunction) {

      if (!allowedBusinessFunctions.includes(requestedBusinessFunction)) {
        return h.response('SANDBOX_ERROR: This endpoint cannot be accessed using the e-RS Business Function provided. Allowed values: ' + allowedBusinessFunctions).code(403)
      }

      if (requestedBusinessFunction === 'SERVICE_PROVIDER_CLINICIAN_ADMIN') {
        if (!oboUserId) {
          return h.response('SANDBOX_ERROR: When this endpoint is accessed using the e-RS SERVICE_PROVIDER_CLINICIAN_ADMIN Business Function then an On-Behalf-Of User ID must be provided').code(403)
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

module.exports = {
    isValidUuid,
    hasLegacyPrefix,
    validateBusinessFunction
};