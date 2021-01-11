'use strict';


/**
 * A001 Create Professional Session
 * As an e-RS user working in an integrated system I want to create a Professional Session in the Spine using my smartcard roles So that I can securely access e-RS functions through my integrated system
 *
 * body Body 
 * token Integer The user ID
 * xAPI_ASID String  (optional)
 * returns inline_response_201
 **/
exports.v1ProfessionalSessionPOST = function(body,token,xAPI_ASID) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = {
  "typeInfo" : "typeInfo",
  "permission" : "",
  "id" : "id",
  "user" : {
    "identifier" : "identifier",
    "firstName" : "firstName",
    "lastName" : "lastName",
    "permissions" : "",
    "middleName" : ""
  },
  "token" : "token"
};
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}

