containerName:=ers-apim-referrals-build
imageName:=ers-apim-referrals-build-image

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

.PHONY: install
install:
	@docker exec -it ${containerName} sh -c "poetry install"
	

.PHONY: bash
bash:
	@docker exec -it ${containerName} sh