const postCreateProfessionalSession = require('./postCreateProfessionalSession')
const getStatus = require('./getStatus')
const getHealth = require('./getHealth')
const getPing = require('./getPing')

const routes = [].concat(postCreateProfessionalSession, getStatus, getHealth, getPing)

module.exports = routes
