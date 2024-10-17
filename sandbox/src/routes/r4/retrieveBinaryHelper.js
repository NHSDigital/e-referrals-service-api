module.exports = [
  /**
   * Sandbox implementation for retrieveBinary (R4) endpoint helper, 
   * with an ObjectStore 'mock', allowing redirection and simple file retrieval.
   */
  {
    method: 'GET',
    path: '/ObjectStore/RetrieveBinary/{fileDownloadUuid}',
    handler: (request, h) => {

      const uuid = request.params.fileDownloadUuid
      const filename = 'example_attachment.pdf'
      const filePath = `./r4/requestUrlForFileDownload/${filename}`
      const responseCode = 200

      if (uuid === 'd497bbe3-f88b-45f1-b3d4-9c563e4c0f5f') {
        return h.file(filePath).code(responseCode).header('Content-Disposition', `attachment; filename*=UTF-8''${filename}`)
          .header('Content-Type', 'application/pdf');
      }
    }
  }
]
