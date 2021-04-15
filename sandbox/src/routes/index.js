const postCreateProfessionalSession = require('./postCreateProfessionalSession')
const getStatus = require('./getStatus')
const getHealth = require('./getHealth')
const getPing = require('./getPing')
const createReferral = require('./createReferral')

const routes = [].concat(postCreateProfessionalSession, getStatus, getHealth, getPing, createReferral)

module.exports = routes
