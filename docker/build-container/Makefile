SHELL=/bin/bash -euo pipefail

containerName:=ers-apim-referrals-build
imageName:=ers-apim-referrals-build-image

define containerExec
	@docker exec -it ${containerName} sh -c "$1"
endef

.PHONY: build
build:
	@echo "Building container: ${containerName}"
	@docker build . --tag ${imageName} --target ${imageName}

.PHONY: run
run: build
	@echo "Starting container. container: ${containerName} sourceRoot: ${sourceRoot}"
# 	Attempt to kill the container if it is currently running, otherwise continue.
	@docker kill ${containerName} || true 
#	Remove the container locally if it already exists, otherwise continue.
	@docker container rm ${containerName} || true
#	Start the container, binding the local git repository to support builds and githook functionality.
	@docker run -d -v ${sourceRoot}:/usr/local/ers/referrals --name ${containerName} ${imageName}
	@echo "Container up and running."

.PHONY: clear
clear:
	@echo "Clearing down and removing build container. container: ${containerName}"
# 	Attempt to kill the container if it is currently running, otherwise continue.
	@docker kill ${containerName} || true 
#	Remove the container locally if it already exists, otherwise continue.
	@docker container rm ${containerName} || true
	@echo "Container removed."

.PHONY: install
install: poetry-install npm-install

.PHONY: poetry-install
poetry-install:
	$(call containerExec,poetry install)

.PHONY: npm-install
npm-install:
	$(call containerExec,npm install)
	
.PHONY: bash
bash:
	@docker exec -it ${containerName} sh

.PHONY: copy-examples
copy-examples:
	$(call containerExec,scripts/copy_examples_from_sandbox.sh)

.PHONY: lint
lint: copy-examples
	$(call containerExec,npm run lint-oas)
	$(call containerExec,cd sandbox && make lint)
	$(call containerExec,poetry run python scripts/xml_validator.py)
	$(call containerExec,poetry run flake8 **/*.py)
	@printf "\nLinting passed.\n\n"

.PHONY: clean
clean:
	$(call containerExec,rm -rf build)
	$(call containerExec,rm -rf dist)
	$(call containerExec,rm -rf specification/components/r4/examples)
	$(call containerExec,rm -rf specification/components/stu3/examples)

.PHONY: serve
serve:
	$(call containerExec,npm run serve)

.PHONY: publish
publish:
	$(call containerExec,mkdir -p build)
	$(call containerExec,npm run publish 2> /dev/null)
	$(call containerExec,poetry run python scripts/validate_oas_examples.py)

.PHONY: python # Opens a python interpreter using the correct virtual environment for the project.
python:
	$(call containerExec,poetry run python)
