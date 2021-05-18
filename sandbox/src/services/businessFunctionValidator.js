
module.exports = {


  hasValidBusinessFunction: function (request, allowedBusinessFunctions) {

    if (request && request.headers["nhsd-ers-business-function"]) {
      return allowedBusinessFunctions.includes(request.headers["nhsd-ers-business-function"])
    }

    return false;

  }

}
