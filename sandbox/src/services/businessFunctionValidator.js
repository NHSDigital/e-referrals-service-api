
module.exports = {


  validateBusinessFunction: function (request, h, allowedBusinessFunctions) {

    if (request && request.headers["nhsd-ers-business-function"]) {

      if (!allowedBusinessFunctions.includes(request.headers["nhsd-ers-business-function"])) {
        return h.response('SANDBOX_ERROR: This endpoint cannot be accessed using the e-RS Business Function provided. Allowed values: ' + allowedBusinessFunctions).code(403);
      }
    }

    return undefined;

  }

}
