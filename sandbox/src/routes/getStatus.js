module.exports = [
  /**
   * GET /_status
   * Returns empty body with 200 response code.
   */
  {
    method: 'GET',
    path: '/_status',
    handler: () => {
      return "";
    }
  }
]
