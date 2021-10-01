# e-Referrals-Service

![Build](https://github.com/NHSDigital/e-referrals-service-api/workflows/Build/badge.svg?branch=master)

This is a RESTful HL7® FHIR® API specification for the *e-Referral-Service Professional API*.

* `specification/` This [Open API Specification](https://swagger.io/docs/specification/about/) describes the endpoints, methods and messages exchanged by the API. Use it to generate interactive documentation; the contract between the API and its consumers.
* `sandbox/` This NodeJS application implements a mock implementation of the service. Use it as a back-end service to the interactive documentation to illustrate interactions and concepts. It is not intended to provide an exhaustive/faithful environment suitable for full development and testing.
* `scripts/` Utilities helpful to developers of this specification.
* `proxies/` Live (connecting to another service) and sandbox (using the sandbox container) Apigee API Proxy definitions.

Consumers of the API will find developer documentation on the [NHS Digital Developer Hub](https://digital.nhs.uk/developer/api-catalogue/e-referral-service-fhir).

## Contributing
Contributions to this project are welcome from anyone, providing that they conform to the [guidelines for contribution](https://github.com/NHSDigital/e-referrals-service-api/blob/master/CONTRIBUTING.md) and the [community code of conduct](https://github.com/NHSDigital/e-referrals-service-api/blob/master/CODE_OF_CONDUCT.md).

### Licensing
This code is dual licensed under the MIT license and the OGL (Open Government License). Any new work added to this repository must conform to the conditions of these licenses. In particular this means that this project may not depend on GPL-licensed or AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).

## Development

### Requirements
* make
* nodejs + npm/yarn
* [poetry](https://github.com/python-poetry/poetry)

### Environment setup
Currently, automation for setting up the right environment is only available for machines based on RedHatEnterpriseLinux (RHEL).
Running the following will ensure your environment is ready for development.
It will install [pyenv](https://github.com/pyenv/pyenv), Python 3.8.2 and its dependencies (yum), create a virtual environment (named apigee), and ensure poetry is installed under it.
```
$ make setup-environment
```
>Activating apigee is now done by the file .python-version, so cd'ing into the repository directory will suffice to use the virtual environment.

If you wish to remove all changes made by setup-environment, you can run the following:
```
$ make clean-environment
```
> This will erase your ~/.pyenv directory, where pyenv stores the different Python versions, and will revert ~/.bashrc and ~./bash_profile. You may want to logout/login for changes to take effect.

### Install
After setting up and activating the right environment, running make install will set up additional configuration pertaining to node, poetry and githooks.
```
$ make install
```

> #### Updating hooks
> You can install/update some pre-commit hooks to ensure you can't commit invalid spec changes by accident. These are also run in CI, but it's useful to run them locally too.
>
>```
>$ make install-hooks
>```

### Environment Variables
Various scripts and commands rely on environment variables being set. These are documented with the commands.

:bulb: Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

### Make commands
There are `make` commands that alias some of this functionality:
 * `lint` -- Lints the spec and code
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format

### Testing
Each API and team is unique. We encourage you to use a `test/` folder in the root of the project, and use whatever testing frameworks or apps your team feels comfortable with. It is important that the URL your test points to be configurable. We have included some stubs in the Makefile for running tests.

### VS Code Plugins

 * [openapi-lint](https://marketplace.visualstudio.com/items?itemName=mermade.openapi-lint) resolves links and validates entire spec with the 'OpenAPI Resolve and Validate' command
 * [OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) provides sidebar navigation


### Emacs Plugins

 * [**openapi-yaml-mode**](https://github.com/esc-emacs/openapi-yaml-mode) provides syntax highlighting, completion, and path help

### Speccy

> [Speccy](http://speccy.io/) *A handy toolkit for OpenAPI, with a linter to enforce quality rules, documentation rendering, and resolution.*

Speccy does the lifting for the following npm scripts:

 * `test` -- Lints the definition
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format

(Workflow detailed in a [post](https://developerjack.com/blog/2018/maintaining-large-design-first-api-specs/) on the *developerjack* blog.)

:bulb: The `publish` command is useful when uploading to Apigee which requires the spec as a single file.

### Caveats

#### Swagger UI
Swagger UI unfortunately doesn't correctly render `$ref`s in examples, so use `speccy serve` instead.

#### Apigee Portal
The Apigee portal will not automatically pull examples from schemas, you must specify them manually.

## Deployment

### Specification
Update the API Specification and derived documentation in the Portal.

`make deploy-spec` with environment variables:

* `APIGEE_USERNAME`
* `APIGEE_PASSWORD`
* `APIGEE_SPEC_ID`
* `APIGEE_PORTAL_API_ID`

### API Proxy & Sandbox Service
Redeploy the API Proxy and hosted Sandbox service.

`make deploy-proxy` with environment variables:

* `APIGEE_USERNAME`
* `APIGEE_PASSWORD`
* `APIGEE_ORGANIZATION`
* `APIGEE_ENVIRONMENTS` - Comma-separated list of environments to deploy to (e.g. `test,prod`)
* `APIGEE_APIPROXY` - Name of the API Proxy for deployment
* `APIGEE_BASE_PATH` - The proxy's base path (must be unique)

:bulb: Specify your own API Proxy (with base path) for use during development.

#### Platform setup

Successful deployment of the API Proxy requires:

 1. A *Target Server* named `e-referrals-service-api-target`
 2. A *Key-Value Map* named `ers-variables`, containing any values you might need at proxy runtime
 2. A *Key-Value Map* named `ers-variables-encrypted`, containing any secrets you might need at proxy runtime

:bulb: For Sandbox-running environments (`test`) these need to be present for successful deployment but can be set to empty/dummy values.
