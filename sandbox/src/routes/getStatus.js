module.exports = [
  /**
   * GET /_status
   * Returns empty body with 200 response code.
   */
  {
    method: 'GET',
    path: '/_status',
    handler: (request, h) => {
      return h.response(
        {
          "status": "pass",
          "date": Date.now()
        });
    }
  }
]
