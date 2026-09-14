const OBJECT_STORE_FILE_ID = 'd497bbe3-f88b-45f1-b3d4-9c563e4c0f5f'
const DEFAULT_UPLOAD_FILENAME = 'upload.bin'

function stripTrailingSlash(url) {
  return url.replace(/\/+$/, '')
}

function getObjectStoreLocation(request) {
  const explicitBaseUrl = request.headers['x-ers-sandbox-baseurl']
  const baseUrl = typeof explicitBaseUrl === 'string' && explicitBaseUrl.trim()
    ? stripTrailingSlash(explicitBaseUrl.trim())
    : stripTrailingSlash(request.server.info.uri)

  return `${baseUrl}/ObjectStore/${OBJECT_STORE_FILE_ID}`
}

function createContentDisposition(fileNameHeaderValue) {
  const inputFileName = String(fileNameHeaderValue || '').replace(/[\r\n]/g, '').trim()
  const utf8Filename = inputFileName || DEFAULT_UPLOAD_FILENAME
  const asciiFallback = utf8Filename
    .replace(/[^\x20-\x7E]/g, '_')
    .replace(/["\\]/g, '_')
  const safeFallback = asciiFallback || DEFAULT_UPLOAD_FILENAME
  const encodedFilename = encodeURIComponent(utf8Filename)

  return `attachment; filename="${safeFallback}"; filename*=UTF-8''${encodedFilename}`
}

module.exports = {

  getExampleResponseForRetrieveBusinessFunctions: function () {

    return { responsePath: 'r4/retrieveBusinessFunctions/responses/PractitionerRoleBundle.json', responseCode: 200 }
  },

  getExampleResponseForRetrieveOboUsers: function () {
    return { responsePath: 'r4/retrieveOboUsers/responses/PractitionerBundle.json', responseCode: 200 }
  },

  getExampleResponseForGetHealthcareService: function (request) {
    const version = request.params.version
    const serviceId = request.params.serviceId

    if (serviceId == 1 && (!version || version == 1)) {
      return 'r4/getService/responses/sampleServiceWithMinimumAttributes.json'
    }

    if (serviceId == 2 && (!version || version == 1)) {
      return 'r4/getService/responses/sampleServiceWithFullAttributes.json'
    }
  },

  getExampleResponseForSearchForHealthcareServices: function (request) {
    const ids = request.query['_id']

    if (ids == ['1', '2']) {
      return 'r4/searchForServices/responses/searchServiceWithMinmumalAttributes.json'
    }

    if (ids == ['3', '4']) {
      return 'r4/searchForServices/responses/searchServiceWithMaxAndMinAttributes.json'
    }

    if (ids == ['5', '6']) {
      return 'r4/searchForServices/responses/searchServiceWithEmptyResponse.json'
    }

    return null
  },

  getExampleResponseForSearchServiceRequest: function (request) {
    let ubrn;
    const identifier = request.query.identifier;

    if (identifier.includes('|')) {
      ubrn = identifier.split('|')[1]
    }
    else {
      ubrn = identifier
    }

    if (ubrn === '000000070000') {
      return 'r4/searchServiceRequest/responses/ResponseExampleReferral.json'
    }
    else if (ubrn === '000000070001') {
      return 'r4/searchServiceRequest/responses/ResponseExampleAdvice.json'
    }
    else if (ubrn === '000000070002') {
      return 'r4/searchServiceRequest/responses/ResponseExampleReferralAndAdvice.json'
    }
    else if (ubrn === '000000070003') {
      return 'r4/searchServiceRequest/responses/ResponseExampleEmpty.json'
    }

    return null
  },

  getExampleResponseForUploadFileToDocumentStore: function (request) {
    const filename = request.headers['nhsd-ers-file-name']
    const fileSize = request.headers['nhsd-ers-file-size']
    const fileMimeType = request.headers['nhsd-ers-file-mime-type']

    if (filename && fileSize && fileMimeType) {
      return {
        responsePath: 'r4/uploadFileToDocumentStore/responses/BinaryResource.json',
        responseCode: 200,
        location: getObjectStoreLocation(request),
        contentDisposition: createContentDisposition(filename)
      }
    }

    return null
  }
}
