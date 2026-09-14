---
applyTo: "sandbox/**"
description: "Sandbox mock server architecture, route handler patterns, mock response provider, and how to add new endpoints"
---

# Sandbox Architecture

The sandbox is a **Hapi.js (v21)** mock server that simulates the e-RS FHIR API. It returns static fixture data and never connects to the real backend.

## Structure

| Path | Purpose |
|---|---|
| `sandbox/src/app.js` | Server entry point — port 9000, CORS config, common response headers |
| `sandbox/src/routes/index.js` | Aggregates all route handlers from `stu3/` and `r4/` subdirectories |
| `sandbox/src/routes/stu3/` | STU3 FHIR endpoint handlers (one file per endpoint) |
| `sandbox/src/routes/r4/` | R4 FHIR endpoint handlers |
| `sandbox/src/routes/common/validationUtils.js` | Shared validation utilities (business function checks, UUID validation) |
| `sandbox/src/routes/stu3/services/mockResponseProvider.js` | Maps request bodies/parameters to fixture file paths for STU3 |
| `sandbox/src/mocks/` | Static JSON/text fixtures organised by FHIR version and endpoint |
| `sandbox/src/routes/objectStore.js` | Handles `/ObjectStore` routes for file upload/download |
| `sandbox/Dockerfile` | Container build — runs on port 9000 |

## Common response headers

`app.js` adds these to every response via an `onPreResponse` extension:
- `X-Correlation-ID` — echoed from the request's `x-correlation-id` header
- `X-Request-ID` — fixed value `58621d65-d5ad-4c3a-959f-0438e355990e-1` (except ObjectStore routes)

## Route handler pattern

Every route handler follows the same structure:

```javascript
const mockResponseProvider = require('./services/mockResponseProvider')
const validationUtils = require('../common/validationUtils')

function handleEndpoint(request, h) {
  // 1. Define allowed business functions for this endpoint
  const allowedBusinessFunctions = ["REFERRING_CLINICIAN", "SERVICE_PROVIDER_CLINICIAN"]

  // 2. Validate business function header — returns 403 if not in allowed list
  const validationResult = validationUtils.validateBusinessFunction(request, h, allowedBusinessFunctions)
  if (validationResult) return validationResult

  // 3. Use mockResponseProvider to map request → fixture file path
  const { responsePath } = mockResponseProvider.getExampleResponseForX(request)
  if (responsePath != null) {
    return h.file(responsePath, { etagMethod: false }).code(200).type("application/fhir+json")
  }

  // 4. Fall back to error fixture if no match
  return h.file('stu3/STU3-SandboxErrorOutcome.json').code(422)
}

// 5. Export as Hapi route array
module.exports = [
  { method: 'GET', path: '/FHIR/STU3/Resource/{id}', handler: (request, h) => handleEndpoint(request, h) }
]
```

## Mock response provider (`mockResponseProvider.js`)

This module maps request inputs to response fixtures. Two main patterns:

### POST endpoints (request body matching)
```javascript
mapExampleResponse(request, {
  'src/mocks/stu3/endpoint/requests/Request.json': 'stu3/endpoint/responses/Response.json'
})
```
Uses `lodash.isEqual` to deep-compare the incoming request body against stored example request bodies. If a match is found, returns the corresponding fixture path.

### GET endpoints (parameter matching)
```javascript
mapExampleGetResponse(parameterValue, {
  'paramValue': 'stu3/endpoint/responses/Response.json'
})
```
Simple key-value lookup by a request parameter or header value.

### Business function branching
Many handlers select different response maps based on the `nhsd-ers-business-function` header, returning different fixtures for different user roles.

## Business function validation

`validationUtils.validateBusinessFunction()` checks:
1. The `nhsd-ers-business-function` header is in the endpoint's allowed list → 403 if not
2. If `SERVICE_PROVIDER_CLINICIAN_ADMIN`, an `nhsd-ers-on-behalf-of-user-id` header must be present → 403 if missing
3. For all other roles, `nhsd-ers-on-behalf-of-user-id` must NOT be present → 403 if provided

## Mock fixture organisation

```
sandbox/src/mocks/
├── stu3/
│   ├── createReferral/
│   │   ├── requests/       # Example request bodies for matching
│   │   └── responses/      # Response fixtures
│   ├── retrieveWorklist/
│   └── ...
├── r4/
│   ├── retrieveBusinessFunctions/
│   └── ...
└── NotFoundOutcome.txt     # Generic 404 response
```

Fixtures serve as the **source of truth** for both the sandbox and the OAS spec examples — `make copy-examples` copies them into `specification/components/*/examples/`.

## Running the sandbox

- **Docker**: `make sandbox` (builds and runs on port 9100→9000)
- **Direct**: `cd sandbox && npm start` (runs on port 9000)
- **Debug**: `cd sandbox && npm run debug` (with Node.js inspector on port 9229)

## Adding a new sandbox endpoint

1. Create a response fixture in `sandbox/src/mocks/{stu3,r4}/endpointName/responses/`
2. If a POST endpoint, create example request bodies in `.../requests/`
3. Add a response mapping function in `mockResponseProvider.js` (or equivalent for R4)
4. Create a route handler file in `sandbox/src/routes/{stu3,r4}/endpointName.js` following the pattern above
5. Import and add the route to the array in `sandbox/src/routes/index.js`
6. Run `make copy-examples` then `make lint` to validate
