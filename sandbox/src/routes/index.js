const postCreateProfessionalSession = require('./postCreateProfessionalSession')
const getStatus = require('./getStatus')
const getHealth = require('./getHealth')

const routes = [].concat(postCreateProfessionalSession, getStatus, getHealth)

module.exports = routes
