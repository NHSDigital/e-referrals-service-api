SHELL=/bin/bash -euo pipefail

install:
	 npm install

lint:
	npm run lint-js

build:
	docker build -t e-referrals-service-api-sandbox .

run:
	docker run -p 9000:9000 e-referrals-service-api-sandbox:latest

