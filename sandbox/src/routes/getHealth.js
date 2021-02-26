module.exports = [
  /**
   * GET /_helath
   * Returns empty body with 200 response code.
   */
  {
    method: 'GET',
    path: '/_health',
    handler: (request, h) => {
      return h.response().code(200)
    }
  }
]
