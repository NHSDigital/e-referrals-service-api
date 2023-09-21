SHELL=/bin/bash -euo pipefail

containerName := ers-apim-referrals-build
imageName := ers-apim-referrals-build-image

#	Add additional docker args as required.
ifdef ${environment}
	dockerArgs := ${dockerArgs} -e ENVIRONMENT=${environment}
endif
ifdef ${serviceBasePath}
	dockerArgs := ${dockerArgs} -e SERVICE_BASE_PATH=${serviceBasePath}
endif

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
	@docker run -d -v ${sourceRoot}:/usr/local/ers/referrals \
		-p 127.0.0.1:9001:9001 \
		--network=${network} \
		${dockerArgs} --name ${containerName} ${imageName}
	@echo "Container up and running."

.PHONY: clear
clear:
	@echo "Clearing down and removing build container. container: ${containerName}"
# 	Attempt to kill the container if it is currently running, otherwise continue.
	@docker kill ${containerName} || true 
#	Remove the container locally if it exists, otherwise continue.
	@docker container rm ${containerName} || true
	@echo "Container removed."
	@echo "Removing image..."
	@docker rmi ${imageName} || true
	
.PHONY: bash
bash:
	@docker exec -it ${containerName} sh

.PHONY: stop
stop:
	@echo "Stopping the build container..."
	@docker kill ${containerName}
	@echo "Container stopped."

.PHONY: python
python:
	@docker exec -it ${containerName} sh -c "poetry run python ${command}"
