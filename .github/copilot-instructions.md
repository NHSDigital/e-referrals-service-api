# e-Referrals Service API — Copilot Context

## What is this repo?

This is the **e-Referral Service (e-RS) FHIR API** maintained by NHS Digital. It provides RESTful endpoints for creating paperless referrals from primary to secondary care. The repo contains the OpenAPI specification, an Apigee API proxy layer, a Node.js sandbox (mock server), and Python-based test suites.

This repo is the **API layer** — it does NOT contain the e-RS core application. The Apigee proxy forwards authenticated requests to the real e-RS backend at `/ers-api`. The sandbox returns fixture data for development and never touches the real backend.

The live API documentation is published to the [NHS Developer Hub](https://digital.nhs.uk/developer/api-catalogue/e-referral-service-fhir).

## Sibling repository

This repo has a sibling: **`e-referrals-service-patient-care-api`**. Both repos follow the same structure and procedures (environment setup, `make publish`, release process). If you know how to work in one, you can work in the other.

## Repository structure

| Directory | Purpose |
|---|---|
| `specification/` | OpenAPI 3.0 spec with components split across `components/r4/` (FHIR R4) and `components/stu3/` (FHIR STU3) |
| `sandbox/` | Node.js (Hapi) mock server. Entry: `sandbox/src/app.js`. Routes: `sandbox/src/routes/{stu3,r4}/`. Fixtures: `sandbox/src/mocks/` |
| `proxies/live/` | Production Apigee proxy (~60 policies: OAuth, ASID, ODS allowlist, rate limiting, header swapping) |
| `proxies/sandbox/` | Lightweight Apigee proxy (~11 policies, no auth) forwarding to the mock server |
| `tests/` | Python pytest suites: `sandbox/`, `integration/`, `smoke/` |
| `terraform/` | Apigee infrastructure-as-code using `api-platform-service-module` |
| `scripts/` | Build & dev utilities |
| `azure/` | Azure DevOps CI/CD pipeline definitions |
| `build/` | Generated output — bundled single-file OAS JSON |

## FHIR versions

- **STU3** — the original version, most endpoints live here
- **R4** — newer endpoints (business functions, healthcare services, service requests, attachments)

Routes, schemas, examples, and tests all mirror this split.

## Package management

| Ecosystem | Tool | Config file | Install |
|---|---|---|---|
| Python | **Poetry** (package-mode=false) | `pyproject.toml` / `poetry.lock` | `poetry install` |
| Node (root) | **npm** | `package.json` | `npm install` |
| Node (sandbox) | **npm** | `sandbox/package.json` | `cd sandbox && npm install` |

- Python ≥ 3.13 required
- Root `package.json` is only `@redocly/cli` for OAS linting/bundling
- `make install` installs all three plus git hooks

## Key make targets

```
make clean-environment    # Delete the pyenv 'apigee' virtual environment
make setup-environment    # Bootstrap dev environment (pyenv, Python 3.13, dependencies) — run in a NEW terminal after
make install              # Install all deps (node + poetry + git hooks)
make lint                 # Lint OAS spec, sandbox JS, XML proxies, Python
make publish              # Bundle OAS spec → build/e-referrals-service-api.json
make serve                # Preview spec docs on port 5000
make sandbox              # Build & run sandbox Docker container (port 9100→9000)
make sandbox-tests        # Run sandbox pytest suite
make release              # Full release build
```

## Environment setup (first time / reset)

1. `make clean-environment` — removes the pyenv `apigee` virtual environment (skip on first setup)
2. Open a **new terminal** (so shell profile changes take effect)
3. `make setup-environment` — installs pyenv, Python 3.13, creates the `apigee` venv, installs Poetry
4. Open a **new terminal** again
5. `pyenv version` — should show `apigee`. If not, repeat steps 1–4
6. `make install` — installs Node deps (root + sandbox) and Poetry deps + git hooks

The `.python-version` file auto-activates the `apigee` venv when you `cd` into the repo.

## Release process

1. `make publish` — bundles the OAS spec into a single JSON file:
   - Redocly CLI reads `specification/e-referrals-service-api.yaml`, resolves all `$ref`s, dereferences, and removes unused components
   - Piped through `scripts/set_version.py` — calculates the version from git commit messages (using `+major`, `+minor`, `+setstatus` commands in commit messages) and injects it into `info.version`
   - Piped through `scripts/populate_placeholders.py` — replaces `[[HYPERLINK_*]]` placeholders with actual markdown links for the Developer Hub
   - Output: `build/e-referrals-service-api.json` — this is the OAS file that goes into Apigee
2. `make release` — runs `clean` → `publish` → `build_proxy` → packages everything into `dist/`
3. Deployment is handled by the release management process (not individual developers) — the Azure DevOps release pipeline is triggered by a `v*` tag push, which deploys to Apigee environments

## CI/CD

- **Azure DevOps** pipelines in `azure/` — build, PR validation, release
- Extends shared templates from `NHSDigital/api-management-utils`
- Release pipeline packages spec + proxies + tests into `dist/`
- GitHub has `dependabot.yml` for dependency updates and PR/issue templates

## Branching

- **develop** — default working branch; create PRs from here
- **master** — release branch; merges to master are part of the release process

## Licensing

Dual licensed MIT + OGL (Open Government License). **No GPL or AGPL dependencies allowed** — this would violate the terms of those libraries' licenses. Check before adding any new package.

## Deeper context

Detailed context for specific areas is split into separate instruction files that load automatically when you're working in the relevant part of the codebase:

- `proxies/**` → proxy architecture, request flow, policies, shared flows
- `sandbox/**` → sandbox architecture, route handler patterns, mock response provider
- `tests/**` → test structure, Actor model, activity codes, SandboxTest base class
- `specification/**` → OAS workflow, examples pipeline, Redocly config
