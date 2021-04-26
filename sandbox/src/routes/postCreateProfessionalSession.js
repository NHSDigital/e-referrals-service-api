module.exports = [
  /**
   * POST to /submission
   * If createProfessionalSessionResponse.json file exists in `mock` directory then that will be the response otherwise, 404
   */
  {
    method: '*',
    path: '/v1/ProfessionalSession',
    handler: (request, h) => {
      if (request.raw.req.method !== 'POST') {
        const responseMessage = {
          error: `Request method must be POST, not ${request.raw.req.method}`
        } ;
        return h.response(responseMessage).code(405)
      }

      const path = 'createProfessionalSessionResponse.json'
      return h.file(path)
    }
  }
]
