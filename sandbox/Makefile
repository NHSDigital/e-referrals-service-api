SHELL=/bin/bash -euo pipefail

.PHONY: install lint build run clean

install:
	 npm install

lint:
	npm run lint-js

build:
	docker build -t e-referrals-service-api-sandbox .

run:
	docker run -p 9100:9000 e-referrals-service-api-sandbox:latest

clean:
	docker stop $$(docker ps -a | awk '$$2 ~ /e-referrals-service-api-sandbox/ {print $$1}') || /bin/true
	docker rm $$(docker ps -a | awk '$$2 ~ /e-referrals-service-api-sandbox/ {print $$1}') || /bin/true
	docker rmi e-referrals-service-api-sandbox || /bin/true
