.PHONY: help

help:
	@echo "Type make, then hit tab to see make options"

setup_env:
	## Copy but don't overwrite the docker env
	cp -n docker/docker.env.sample docker/docker.env || true

build:
	docker-compose build

run:
	docker-compose up

up:
	docker-compose up -d

down:
	docker-compose down

shell:
	@echo "Opening shell in docker container"
	@echo "Use this shell to run python and django commands normally"
	@docker-compose exec web bash

web: run

migrate:
	docker-compose exec web python manage.py migrate auth || true
	docker-compose exec web python manage.py migrate

test:
	docker-compose exec web pytest -v chipy_org/

lint:
	docker-compose exec web pylint chipy_org/

setup: setup_env build
