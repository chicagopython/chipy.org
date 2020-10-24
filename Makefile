.PHONY: help
date_tag=$(shell date +%Y%m%d%H%M)

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

psql:
	@docker-compose exec db psql chipy chipy

resetdb:
	@docker-compose exec db psql chipy chipy -c "drop schema if exists public cascade;"
	@docker-compose exec db psql chipy chipy -c "create schema public;"

web: run

migrate:
	docker-compose exec web python manage.py migrate auth || true
	docker-compose exec web python manage.py migrate

migration:
	docker-compose exec web python manage.py makemigrations -n $(name) $(app)

tag:
	echo Making tag $(date_tag)
	git tag -m $(date_tag) $(date_tag)

test:
	docker-compose exec web pytest -v chipy_org/

lint:
	docker-compose exec web pylint -j 0 chipy_org/

format:
	docker-compose exec web isort -rc -tc --atomic .
	docker-compose exec web black .

format-check:
	docker-compose exec web isort -rc -tc --atomic --diff .
	docker-compose exec web black --diff .

setup: setup_env build

superuser:
	docker-compose exec web ./manage.py createsuperuser

tail-logs:
	docker-compose logs -f web
