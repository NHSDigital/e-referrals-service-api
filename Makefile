SHELL=/bin/bash -euo pipefail

install: install-node install-poetry install-hooks

install-poetry:
	poetry install

install-node:
	npm install
	cd sandbox && npm install

install-hooks:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod u+x .git/hooks/pre-commit

lint: copy-examples
	npm run lint-oas
	cd sandbox && make lint
	poetry run python scripts/xml_validator.py
	poetry run flake8 **/*.py
	@printf "\nLinting passed.\n\n"

clean:
	rm -rf build
	rm -rf dist
	rm -rf specification/components/examples

publish: clean copy-examples
	mkdir -p build
	npm run publish 2> /dev/null
	poetry run python scripts/validate_oas_examples.py

copy-examples:
	scripts/copy_examples_from_sandbox.sh

serve:
	npm run serve

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
	cp manifest_template_macros.yml dist/manifest_template_macros.yml

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

.PHONY: setup-environment clean-environment sandbox
