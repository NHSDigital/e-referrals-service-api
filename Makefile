SHELL=/bin/bash -euo pipefail

install: start-container install-hooks

install-hooks:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod u+x .git/hooks/pre-commit

lint: copy-examples
	$(MAKE) -C docker/build-container lint

clean:
	$(MAKE) -C docker/build-container clean

publish: clean copy-examples
	$(MAKE) -C docker/build-container publish

copy-examples:
	$(MAKE) -C docker/build-container copy-examples

serve:
	$(MAKE) -C docker/build-container serve

check-licenses:
	npm run check-licenses
	scripts/check_python_licenses.sh

sandbox: publish
	$(MAKE) -C sandbox/ build run

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

test:
	echo "TODO: add tests"

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
	$(MAKE) -C docker/build-container install


install-container:
	@echo "Installing dependencies within build container..."
	$(MAKE) -C docker/build-container install

remove-container:
	$(MAKE) -C docker/build-container clear

bash:
	$(MAKE) -C docker/build-container bash

python:
	$(MAKE) -C docker/build-container python

.PHONY: setup-environment clean-environment sandbox start-container install-container bash python
