const postCreateProfessionalSession = require('./postCreateProfessionalSession')
const getStatus = require('./getStatus')

const routes = [].concat(postCreateProfessionalSession, getStatus)

module.exports = routes
