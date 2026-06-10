---
applyTo: "specification/**"
description: "OAS spec workflow, examples pipeline, Redocly config, and how to add or modify API specification"
---

# OpenAPI Specification

The API contract is defined in `specification/e-referrals-service-api.yaml` (OpenAPI 3.0) with components split by FHIR version.

## Structure

```
specification/
├── e-referrals-service-api.yaml     # Root spec file (paths, info, servers)
└── components/
    ├── r4/
    │   ├── schemas/                  # FHIR R4 JSON Schema definitions
    │   └── examples/                 # R4 example responses (copied from sandbox)
    └── stu3/
        ├── schemas/                  # FHIR STU3 JSON Schema definitions
        └── examples/                 # STU3 example responses (copied from sandbox)
```

## Examples pipeline

**Sandbox fixtures are the source of truth for OAS examples.** The flow:

1. Author/update mock response fixtures in `sandbox/src/mocks/{stu3,r4}/`
2. Run `make copy-examples` — this runs `scripts/copy_examples_from_sandbox.sh`, which copies fixtures into `specification/components/{r4,stu3}/examples/`
3. The spec YAML files `$ref` these example files
4. `make publish` bundles everything into a single dereferenced JSON file

This means you should **never edit example files directly** in `specification/components/*/examples/` — they'll be overwritten. Edit the sandbox mocks instead.

## Publishing workflow

`make publish` runs this pipeline:

1. `mkdir -p build`
2. `redocly bundle specification/e-referrals-service-api.yaml --dereferenced --remove-unused-components --ext json` — resolves all `$ref`s into a single file
3. Pipes through `scripts/set_version.py` — injects the calculated version number
4. Pipes through `scripts/populate_placeholders.py` — replaces `[[HYPERLINK_*]]` placeholders with actual URLs
5. Output: `build/e-referrals-service-api.json`

## Linting

`make lint` runs `redocly lint` using the config in `redocly.yaml`:
- Extends the `recommended` ruleset
- Disables `no-invalid-media-type-examples` and `tag-description`

## Previewing docs

`make serve` runs `redocly preview-docs` on port 5000 against the bundled spec.

## Modifying the spec

1. Edit `specification/e-referrals-service-api.yaml` for paths/operations, or component files for schemas
2. Keep schemas split by FHIR version in `components/{r4,stu3}/schemas/`
3. If adding new response examples, create the fixture in `sandbox/src/mocks/` first, then `make copy-examples`
4. Run `make lint` to validate
5. Run `make publish` to generate the bundled output
6. `make serve` to preview the rendered docs

## Version management

The version in the spec's `info.version` field is a placeholder — `scripts/set_version.py` replaces it during the publish step.

Version is calculated automatically from **git commit messages** by `scripts/calculate_version.py`. Embed commands in commit messages to control versioning:

| Command | Effect |
|---|---|
| `+major` | Increment the major version |
| `+minor` | Increment the minor version |
| `+setstatus <status>` | Set the prerelease status (e.g. `alpha`, `beta`) |
| `+clearstatus` | Clear the prerelease status |
| `+startversioning` | Reset version to `v1.0.0-alpha` |

Example commit: `+minor APM-123 Add new endpoint for service requests`

Without any command, the patch version increments automatically.

## Placeholder substitution

`scripts/populate_placeholders.py` replaces `[[HYPERLINK_*]]` tokens (e.g. `[[HYPERLINK_A004]]`, `[[HYPERLINK_A011]]`) in the bundled spec with markdown anchor links for the Developer Hub documentation. These map activity codes to their rendered API endpoint anchors.
