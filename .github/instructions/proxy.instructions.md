---
applyTo: "proxies/**"
description: "Apigee proxy architecture, request flow, policies, shared flows, and how to modify proxy configuration"
---

# Apigee Proxy Architecture

The `proxies/` directory contains two independent Apigee API proxy bundles that share the same base path (`{{ SERVICE_BASE_PATH }}` → `/referrals`).

## `proxies/live/` — production proxy

Forwards requests to the real e-RS backend. This is the most policy-heavy part of the repo.

### Layout

| Path | Purpose |
|---|---|
| `apiproxy/ers.xml` | Root proxy descriptor |
| `apiproxy/proxies/default.xml` | ProxyEndpoint — inbound routing (`_ping`, `_status`, catch-all to target) |
| `apiproxy/targets/ers-target.xml` | TargetEndpoint — outbound to backend via `{{ ERS_TARGET_SERVER }}`, plus all auth/error handling |
| `apiproxy/policies/` | ~60 XML policy files (see breakdown below) |
| `apiproxy/resources/jsc/` | Inline JavaScript used by policies (`IsFhirR4Path.js`, `SetCurrentTimestamp.js`, `SetStatusResponse.js`) |

### Request flow (PreFlow on TargetEndpoint)

1. `javascript.IsFhirR4Path` — sets `isFhirR4Path` boolean by matching `/FHIR/R4/` in the path suffix; this flag drives R4-vs-STU3 branching throughout
2. `OauthV2.VerifyAccessToken` — validates OAuth2 token; accepted scopes: `app:level3`, `user-nhs-id:aal3`, `user-nhs-id:aal2`
3. `FlowCallout.ExtendedAttributes` + `FlowCallout.EUOAllowlistVerify` — (user-restricted only, excluding `/FHIR/R4/PractitionerRole`) validates the end-user organisation ODS code against an allowlist
4. ASID validation — `RaiseFault.MissingAsid` if `app.asid` is empty; then `AssignMessage.PopulateAsidFromApp` + `AssignMessage.SetAsidHeader` copy the ASID onto the request
5. `AssignMessage.AddBaseUrlHeader` — adds the base URL header for the backend
6. `FlowCallout.ApplyRateLimiting` — spike arrest + quota enforcement (delegates to external shared flow — rate/quota values are NOT in this repo)

### Shared flows (external dependencies)

Several `FlowCallout.*` policies delegate to shared flows that are NOT defined in this repo:
- `ApplyRateLimiting` — spike arrest and quota enforcement (rate/quota values configured externally)
- `ExtendedAttributes` — retrieves extended app attributes
- `EUOAllowlistVerify` — validates ODS code against the end-user organisation allowlist
- `LogToSplunk` — audit logging

These shared flows are deployed separately to the Apigee environment. This repo only controls *when* they are called and *how* their errors are handled.

### Conditional flows (TargetEndpoint)

- **`user-restricted-flow`** (`accesstoken.auth_type == "user"`) — rejects app-only business functions (`AUTHORISED_APPLICATION`), swaps NHSD headers from external to internal naming, sets AAL/IAL/AMR headers, and enforces IAL ≥ 3
- **`app-restricted-flow`** (`accesstoken.auth_type == "app"`) — rejects any manually-set `x-ers-*` headers (403), then sets fixed app-restricted values for ODS, business function, user-id, and access-mode
- **`undefined-flow`** — catch-all that returns 403 (should never trigger)

Both flows finish with `AssignMessage.Swap.CorrelationHeader` which converts `X-Correlation-ID` → `NHSD-Correlation-ID` for the backend.

### Header transformation mapping

The proxy swaps external consumer-facing headers to internal backend headers:

| External header (consumer sends) | Internal header (backend receives) |
|---|---|
| `X-Correlation-ID` | `NHSD-Correlation-ID` (appended with `.{messageid}`) |
| `nhsd-end-user-organisation-ods` | `x-ers-ods-code` |
| `nhsd-ers-business-function` | `x-ers-business-function` |
| `nhsd-ers-comm-rule-org` | `x-ers-comm-rule-org` |
| `nhsd-ers-file-name` | `x-ers-file-name` |
| `nhsd-ers-referral-id` | `x-ers-referral-id` |
| `NHSD-eRS-On-Behalf-Of-User-ID` | `x-ers-on-behalf-of-user-id` |

Additional headers set by the proxy (not from consumer input):
- `x-ers-access-mode` — `user` or `app`
- `x-ers-user-id` — from OAuth token (user) or app config (app)
- `x-ers-authentication-assurance-level` — from token
- `x-ers-id-assurance-level` — from token
- `x-ers-amr` — authentication method reference from token

### Response flow

- Sets `X-Request-ID` flag, swaps `x_ers_transaction_id` to the response, removes `nhsd-correlation-id` from the response

### FaultRules (TargetEndpoint)

Error responses are FHIR-version-aware — `isFhirR4Path` selects between R4 and pre-R4 `OperationOutcome` response shapes. Handled faults:
- OAuth token failures (scope errors → AAL insufficient)
- Spike arrest / quota exceeded (rate limiting)
- Insufficient IAL (identity assurance level < 3)
- Missing ASID
- Invalid business function
- ODS header missing / not in partner allowlist
- EUO allowlist internal errors (500)

### Backend connection

- Target server: `{{ ERS_TARGET_SERVER }}` (defaults to `e-referrals-service-api`)
- Backend path: `/ers-api`
- TLS enabled; conditional truststore for feature-test (`--ft-`) environments
- I/O timeout: 180 seconds
- Jinja2 templating (`{{ }}` placeholders) is resolved at build time by `scripts/build_proxy.sh`

### Policy naming conventions

- `AssignMessage.Set.*` — set a header/variable to a fixed value
- `AssignMessage.Swap.*` — rename/transform a header between external and internal naming
- `AssignMessage.Remove.*` — strip a header
- `AssignMessage.SetOperationOutcome*` — prepare FHIR OperationOutcome error variables
- `RaiseFault.*` — return an HTTP error status
- `FlowCallout.*` — delegate to a shared flow
- `KeyValueMapOperations.*` — read from Apigee KVM stores

## `proxies/sandbox/` — sandbox proxy

Lightweight proxy that forwards to the sandbox container (Hapi.js mock server) via Apigee hosted targets.

### Key differences from live

- Only ~11 policies (vs ~60 in live) — no OAuth, no ASID, no rate limiting, no header swapping
- Adds CORS preflight handling (`AssignMessage.AddCors` on OPTIONS)
- Uses `DecodeJWT.FromJWTHeader` to decode (but not validate) the JWT for inspection
- Target is `{{ HOSTED_TARGET_CONNECTION }}` — the sandbox container deployed alongside the proxy
- No fault rules or auth enforcement

### Shared structure

Both proxies share `_ping` and `_status` flows — `_ping` returns a canned response directly (no backend call), `_status` uses an API key from KVM + `ServiceCallout.CallHealthcheckEndpoint`.

## Proxy build process

`scripts/build_proxy.sh` copies both proxy bundles into `build/proxies/`, and for sandbox, rsyncs the entire `sandbox/` app into `build/proxies/sandbox/apiproxy/resources/hosted/` so Apigee can run it as a hosted target.

Jinja2 template variables (e.g. `{{ SERVICE_BASE_PATH }}`, `{{ ERS_TARGET_SERVER }}`, `{{ HOSTED_TARGET_CONNECTION }}`) are resolved during the CI/CD pipeline deployment step.

## Infrastructure

- **Apigee** API gateway managed via Terraform (`terraform/main.tf`)
- Uses the `api-platform-service-module` from NHSDigital
- Backend: Azure (`azurerm` state backend)
- Proxy type auto-selects `sandbox` or `live` based on Apigee environment name

## Adding or modifying a proxy policy

1. Create/edit the XML file in `proxies/live/apiproxy/policies/` (or `sandbox/`)
2. Reference it by `<Name>` in the appropriate flow in `proxies/default.xml` or `ers-target.xml`
3. If it uses JavaScript, add the `.js` file to `apiproxy/resources/jsc/` and reference via `<ResourceURL>jsc://filename.js</ResourceURL>`
4. Run `make lint` — validates all proxy XML via `scripts/xml_validator.py`
5. Remember to handle both R4 and pre-R4 paths if the policy produces FHIR error responses
