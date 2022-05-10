module.exports = [
  /**
   * Sandbox implementation for retrieveBinary (R4) endpoint helper, 
   * with an ObjectStore mock, allowing redirection and example file retrieval.
   */
  {
    method: 'GET',
    path: '/ObjectStore/RetrieveBinary/{fileDownloadUuid}',
    handler: (request, h) => {

      const uuid = request.params.fileDownloadUuid
      const exampleResponsePath = 'retrieveAttachment/responses/example_attachment.pdf'
      const filename = 'example_attachment.pdf'
      const responseCode = 200

      if (uuid === 'd497bbe3-f88b-45f1-b3d4-9c563e4c0f5f') {
        return h.file(exampleResponsePath, {
          mode: 'attachment',
          filename: filename
        }).code(responseCode);
      }
    }
  }
]
