SHELL=/bin/bash -euo pipefail

containerName := e-referrals-service-api-sandbox
imageName := e-referrals-service-api-sandbox

.PHONY: install lint build run clean

install:
	@npm install

lint:
	@npm run lint-js

build:
	@docker build -t ${imageName} .

run:
# 	Attempt to kill the container if it is currently running, otherwise continue.
	@docker kill ${containerName} || true 
#	Remove the container locally if it already exists, otherwise continue.
	@docker container rm ${containerName} || true
	@docker run -d --network=${network} -p 9000:9000 --name ${containerName} ${imageName}
clean:
# 	Attempt to kill the container if it is currently running, otherwise continue.
	@docker kill ${containerName} || true 
#	Remove the container locally if it already exists, otherwise continue.
	@docker container rm ${containerName} || true
#	Remove the image if it exists, otherwise continue.
	@docker rmi ${imageName} || true
