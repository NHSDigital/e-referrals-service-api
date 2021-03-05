const postCreateProfessionalSession = require('./postCreateProfessionalSession')
const postCreateReferralRequest = require('./postCreateReferralRequest')
const echoHeaders = require('./echoSuppliedHeaders')
const getStatus = require('./getStatus')
const getHealth = require('./getHealth')
const getPing = require('./getPing')

const routes = [].concat(postCreateReferralRequest, postCreateProfessionalSession, echoHeaders, getStatus, getHealth, getPing)

module.exports = routes
