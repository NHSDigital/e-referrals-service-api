module.exports = [
  /**
   * Sandbox implementation of an object store.
   */
  {
    method: 'GET',
    path: '/ObjectStore/{fileId}',
    handler: (request, h) => {

      const fileId = request.params.fileId;
      const filePath = '../mocks/r4/retrieveAttachment/example_attachment.pdf';
      const responseCode = 200;

      if (fileId === 'd497bbe3-f88b-45f1-b3d4-9c563e4c0f5f') {
        return h.file(filePath, { etagMethod: false })
                .code(responseCode)
                .header('Content-Disposition', `attachment; filename="=?UTF-8?Q?The_filenam=C3=A9.pdf?="; filename*=UTF-8''The%20filenam%C3%A9.pdf`)
                .header('Content-Type', 'application/pdf');
      }
    }
  }
]
