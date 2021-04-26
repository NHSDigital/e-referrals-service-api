module.exports = [
  /**
   * GET /_ping
   * Returns JSON body with 200 response code.
   */
  {
    method: 'GET',
    path: '/_ping',
    handler: (request, h) => {
      return h.response('{status: 200}').code(200)
    }
  }
]
