/**
 * Sandbox validation for the FHIR R4 Clinical Information Management endpoint.
 * Mirrors the backend's split between structural errors (400) and
 * business-rule errors (422), using the backend's codes and diagnostics.
 */

const COMMENT_URL = 'https://fhir.nhs.uk/StructureDefinition/ers-provider-clinical-information-comment'
const ATTACHMENT_TYPE_SYSTEM = 'https://fhir.nhs.uk/CodeSystem/ers-attachment-type'
const UBRN_SYSTEM = 'https://fhir.nhs.uk/Id/UBRN'
const OPERATION_OUTCOME_PROFILE = 'https://www.hl7.org/fhir/R4/operationoutcome.html'
const HTTP_ERROR_CODES = 'https://fhir.nhs.uk/CodeSystem/http-error-codes'
const ERS_ERROR_CODES = 'https://fhir.nhs.uk/CodeSystem/ers-error-codes'
const MAX_COMMENT_LENGTH = 2000
const MAX_DESCRIPTION_LENGTH = 200

const UUID = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
const UUID_REGEX = new RegExp(`^${UUID}$`)
const BINARY_URL_REGEX = new RegExp(`^Binary/(?:${UUID}|att-[0-9]+-[0-9]+)$`)
const ABSOLUTE_URI_REGEX = /^[a-zA-Z][a-zA-Z0-9+.-]*:\S+$/
const UBRN_REGEX = /^[0-9]{12}$/
const FHIR_DATE_REGEX = /^[0-9]{4}(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01])(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|[+-]((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))?)?)?$/

function operationOutcome(system, code, diagnostics) {
  return {
    resourceType: 'OperationOutcome',
    meta: {
      lastUpdated: new Date().toISOString(),
      profile: [OPERATION_OUTCOME_PROFILE]
    },
    issue: [
      {
        severity: 'error',
        code: 'invalid',
        details: { coding: [{ system, code }] },
        diagnostics
      }
    ]
  }
}

function badRequest(diagnostics) {
  return { responseCode: 400, body: operationOutcome(HTTP_ERROR_CODES, 'REC_BAD_REQUEST', diagnostics) }
}

function unprocessable(diagnostics) {
  return { responseCode: 422, body: operationOutcome(HTTP_ERROR_CODES, 'REC_BAD_REQUEST', diagnostics) }
}

function conflict(diagnostics) {
  return { responseCode: 422, body: operationOutcome(ERS_ERROR_CODES, 'CONFLICTING_VALUES', diagnostics) }
}

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
}

function findCommentExtensions(bundle) {
  return Array.isArray(bundle.extension)
    ? bundle.extension.filter(extension => isObject(extension) && extension.url === COMMENT_URL)
    : []
}

function validateStructure(bundle) {
  if (!isObject(bundle) || bundle.resourceType !== 'Bundle') {
    return badRequest('Bundle.resourceType must be Bundle')
  }
  if (bundle.type !== 'transaction') {
    return badRequest('Bundle.type must be transaction')
  }

  const comments = findCommentExtensions(bundle)
  if (comments.length > 1) {
    return badRequest('Bundle.extension must not contain more than one provider clinical information comment')
  }
  if (comments.length === 1) {
    if (comments[0].valueString === undefined) {
      return badRequest('Bundle.extension.valueString is required for the provider clinical information comment')
    }
    if (typeof comments[0].valueString !== 'string') {
      return badRequest('Bundle.extension.valueString must be a string')
    }
  }

  const entries = Array.isArray(bundle.entry) ? bundle.entry : []
  const fullUrls = new Set()

  for (const entry of entries) {
    if (!isObject(entry) || !isObject(entry.resource)) {
      return badRequest('Bundle.entry.resource is required')
    }

    const transactionRequest = isObject(entry.request) ? entry.request : {}
    if (typeof transactionRequest.method !== 'string' || transactionRequest.method.toUpperCase() !== 'POST') {
      return badRequest('Bundle.entry.request.method must be POST')
    }
    if (transactionRequest.url !== 'DocumentReference') {
      return badRequest('Bundle.entry.request.url must be DocumentReference')
    }

    if (entry.fullUrl !== undefined) {
      const fullUrl = entry.fullUrl
      if (typeof fullUrl !== 'string' || !ABSOLUTE_URI_REGEX.test(fullUrl)) {
        return badRequest('Bundle.entry.fullUrl must be an absolute URI')
      }
      const isUuidUrn = fullUrl.toLowerCase().startsWith('urn:uuid:')
      if (isUuidUrn && !UUID_REGEX.test(fullUrl.substring('urn:uuid:'.length))) {
        return badRequest('Bundle.entry.fullUrl must contain a valid UUID')
      }
      const key = isUuidUrn ? fullUrl.toLowerCase() : fullUrl
      if (fullUrls.has(key)) {
        return badRequest('Bundle.entry.fullUrl must be unique within the Bundle')
      }
      fullUrls.add(key)
    }

    const resource = entry.resource
    if (resource.resourceType !== 'DocumentReference') {
      return badRequest('Bundle.entry.resource must be a DocumentReference')
    }

    const identifier = isObject(resource.subject) && isObject(resource.subject.identifier)
      ? resource.subject.identifier
      : {}
    if (identifier.system !== UBRN_SYSTEM) {
      return badRequest(`DocumentReference.subject.identifier.system must be ${UBRN_SYSTEM}`)
    }
    if (identifier.value === undefined) {
      return badRequest('DocumentReference.subject.identifier.value is required')
    }
    if (typeof identifier.value !== 'string' || !UBRN_REGEX.test(identifier.value)) {
      return badRequest('DocumentReference.subject.identifier.value must be a 12-digit UBRN')
    }

    if (!Array.isArray(resource.content) || resource.content.length !== 1) {
      return badRequest('DocumentReference.content must contain exactly one Binary reference')
    }

    if (resource.date !== undefined &&
      (typeof resource.date !== 'string' || !FHIR_DATE_REGEX.test(resource.date))) {
      return badRequest('DocumentReference.date must be a valid FHIR R4 dateTime')
    }
  }

  return null
}

function validateContent(bundle) {
  const entries = Array.isArray(bundle.entry) ? bundle.entry : []
  if (entries.length === 0) {
    return unprocessable('Bundle.entry must contain at least one DocumentReference')
  }

  const ubrns = new Set(entries.map(entry => entry.resource.subject.identifier.value))
  if (ubrns.size > 1) {
    return unprocessable('Multiple different UBRNs in one transaction')
  }

  const comments = findCommentExtensions(bundle)
  if (comments.length === 1 && comments[0].valueString.length > MAX_COMMENT_LENGTH) {
    return unprocessable(`Bundle.extension.valueString must not exceed ${MAX_COMMENT_LENGTH} characters`)
  }

  const binaryUrls = new Set()
  for (const entry of entries) {
    const resource = entry.resource

    if (resource.status !== 'current') {
      return unprocessable('DocumentReference.status must be current')
    }

    const coding = isObject(resource.type) ? resource.type.coding : undefined
    if (!Array.isArray(coding) || coding.length !== 1 || !isObject(coding[0]) ||
      coding[0].system !== ATTACHMENT_TYPE_SYSTEM || coding[0].code !== 'PROVIDER') {
      return unprocessable('DocumentReference.type must contain exactly one PROVIDER attachment type coding')
    }

    if (resource.description !== undefined &&
      (typeof resource.description !== 'string' || resource.description.length > MAX_DESCRIPTION_LENGTH)) {
      return unprocessable(`DocumentReference.description must not exceed ${MAX_DESCRIPTION_LENGTH} characters`)
    }

    const attachment = isObject(resource.content[0]) ? resource.content[0].attachment : undefined
    const binaryUrl = isObject(attachment) ? attachment.url : undefined
    if (typeof binaryUrl !== 'string' || !BINARY_URL_REGEX.test(binaryUrl)) {
      return unprocessable('DocumentReference.content.attachment.url must reference Binary/{id} where {id} is a UUID or att-{referralId}-{attachmentId}')
    }

    const binaryKey = binaryUrl.toLowerCase()
    if (binaryUrls.has(binaryKey)) {
      return conflict(`${binaryUrl} cannot be linked to the referral more than once`)
    }
    binaryUrls.add(binaryKey)
  }

  return null
}

function getResponse(bundle) {
  const error = validateStructure(bundle) || validateContent(bundle)
  if (error) {
    return error
  }

  return {
    responseCode: 200,
    body: {
      resourceType: 'Bundle',
      type: 'transaction-response',
      entry: bundle.entry.map(() => ({ response: { status: '200 OK' } }))
    }
  }
}

function malformedJsonResponse() {
  return badRequest('Request body must be valid FHIR R4 JSON')
}

module.exports = {
  getResponse,
  malformedJsonResponse
}
