SHELL=/bin/bash -euo pipefail

install:
	 npm install

lint:
	npm run lint

build:
	docker build -t ambulance-analytics-sandbox .

run:
	docker run -p 9000:9000 ambulance-analytics-sandbox:latest

