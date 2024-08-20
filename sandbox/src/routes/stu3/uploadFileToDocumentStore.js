const businessFunctionValidator = require('../../services/businessFunctionValidator')

module.exports = [
  /**
   * Sandbox implementation for uploadFileToDocumentStore endpoint
   */
  {
    method: 'POST',
    path: '/FHIR/STU3/Binary',
    config: {
      payload: {
        maxBytes: 5242880, //5MB
        parse: false,
        // https://nhsd-jira.digital.nhs.uk/browse/ERSSUP-9016 lists currently supported file types
        allow: ['text/plain', 'application/pdf', 'text/xml', 'application/xml', 'text/rtf', 'application/rtf',
          'audio/basic', 'audio/mpeg', 'image/png', 'image/gif', 'image/jpeg',
          'image/tiff', 'video/mpeg', 'application/msword',
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/dicom',
          'message/rfc822']
      }
    },
    handler: (request, h) => {

      const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "REFERRING_CLINICIAN_ADMIN", "SERVICE_PROVIDER_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN_ADMIN"]

      const validationResult = businessFunctionValidator.validateBusinessFunction(request, h, allowedBusinessFunctions)
      if (validationResult) {
        return validationResult
      }

      const filename = request.headers['nhsd-ers-file-name']
      const ubrn = request.headers['nhsd-ers-referral-id']

      // Simply checking if file content is provided along with filename and ubrn header
      if (request.payload && request.payload.length != 0 && filename && ubrn) {
        const response = h.response("").code(201)
        response.headers["Location"] = "Binary/19eb7224-dff3-4730-a5cb-67eac811f1a5";
        return response
      } else {
        return h.file('STU3-SandboxErrorOutcome.json').code(422);
      }

    }
  }
]
