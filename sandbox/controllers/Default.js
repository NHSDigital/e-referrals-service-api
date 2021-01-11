'use strict';

var utils = require('../utils/writer.js');
var Default = require('../service/DefaultService');

module.exports.v1ProfessionalSessionPOST = function v1ProfessionalSessionPOST (req, res, next, body, token, xAPI_ASID) {
  Default.v1ProfessionalSessionPOST(body, token, xAPI_ASID)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};
