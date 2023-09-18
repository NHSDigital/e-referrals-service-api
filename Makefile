SHELL=/bin/bash -euo pipefail

containerName := ers-apim-referrals-build

# Detect if we should be running commands within the container by looking to see if the container is running locally.
USING_CONTAINER := $(shell docker container inspect -f '{{.State.Running}}' $(containerName))
# Whether or not docker commands should be executed with an interactive shell. Can be overridden by supplying INTERACTIVE_SHELL=false when running commands.
INTERACTIVE_SHELL := true

# Manage working within container and outside the container.
ifeq ($(USING_CONTAINER),true)

# Either run commands interactively or not depending on INTERACTIVE_SHELL (defaults to true).
ifeq ($(INTERACTIVE_SHELL),true)

define dexec
	@docker exec -it $(containerName) sh -c "$1"
endef

else

define dexec
	@docker exec $(containerName) $1
endef

endif

# Routes targets to the container where they can be exected as normal.
define dmake
	@echo "Running $1 within container..."
	$(call dexec,make $1)
	@echo "$1 completed successfully within container."
endef

install-poetry:
	$(call dmake,install-poetry)

install-npm:
	$(call dmake,install-npm)

lint:
	$(call dmake,lint)

format-changes:
	$(call dmake,format-changes)

clean:
	$(call dmake,clean)

publish:
	$(call dmake,publish)

copy-examples:
	$(call dmake,copy-examples)

serve:
	$(call dmake,serve)

bash:
	$(MAKE) -C docker/build-container bash

stop-container:
	$(MAKE) -C docker/build-container stop

python: install-poetry ##D Opens a python interpreter within Poetry's virtual environment.
	$(MAKE) -C docker/build-container python

else

install-poetry:
	poetry install

install-npm:
	npm install
	cd sandbox && npm install

lint: copy-examples
	npm run lint-oas
	cd sandbox && make lint
	poetry run python scripts/xml_validator.py
	poetry run flake8 **/*.py
	@printf "\nLinting passed.\n\n"

format-changes:
	scripts/format_changes.sh

clean:
	rm -rf build
	rm -rf dist
	rm -rf specification/components/r4/examples
	rm -rf specification/components/stu3/examples

publish: clean copy-examples
	mkdir -p build
	npm run publish 2> /dev/null
	poetry run python scripts/validate_oas_examples.py

copy-examples:
	scripts/copy_examples_from_sandbox.sh

serve: publish
	npm run serve

endif

install: install-poetry install-npm install-hooks

install-hooks:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod u+x .git/hooks/pre-commit

check-licenses:
	npm run check-licenses
	scripts/check_python_licenses.sh

build-proxy:
	scripts/build_proxy.sh

release: clean publish build-proxy
	mkdir -p dist
	cp -r build/. dist
	cp -R tests dist
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-sandbox.yml
	cp pyproject.toml dist/pyproject.toml
	cp poetry.lock dist/poetry.lock
	cp -R macros dist

sandbox: publish
	$(MAKE) -C sandbox/ build run

setup-environment:
	@if [ -e /usr/bin/yum ]; then \
		scripts/rhel_setup_environment.sh; \
	elif [ -e /usr/local/bin/brew ]; then \
		echo "TODO is Mac"; \
	else \
		echo "Environment not Mac or RHEL"; \
	fi

clean-environment:
	@if [ -e /usr/bin/yum ]; then \
		scripts/rhel_clean_environment.sh; \
	elif [ -e /usr/local/bin/brew ]; then \
		echo "TODO is Mac"; \
	else \
		echo "Environment not Mac or RHEL"; \
	fi

start-container:
	@echo "Attempting to start build container.."
	$(MAKE) -C docker/build-container run sourceRoot=${PWD}
	make USING_CONTAINER=true install-poetry install-npm

remove-container:
	$(MAKE) -C docker/build-container clear

.PHONY: setup-environment clean-environment sandbox start-container remove-container stop-container bash python
