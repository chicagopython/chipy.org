.PHONY: help
help:
	@echo "Type make, then hit tab to see make options"

.PHONY: setup_env
setup_env:
	## Copy but don't overwrite the docker env
	cp --update=none docker/docker.env.sample docker/docker.env || true

.PHONY: build
build:
	docker compose build

.PHONY: run
run:
	docker compose up

.PHONY: up
up:
	docker compose up -d

.PHONY: up-services
up-services:
	docker compose up -d db

.PHONY: down
down:
	docker compose down

.PHONY: shell
shell:
	@echo "Opening shell in docker container"
	@echo "Use this shell to run python and django commands normally"
	@docker compose exec web bash

.PHONY: psql
psql:
	@docker compose exec db psql chipy chipy

.PHONY: resetdb
resetdb:
	@docker compose exec db psql chipy chipy -c "drop schema if exists public cascade;"
	@docker compose exec db psql chipy chipy -c "create schema public;"

.PHONY: web
web: run

.PHONY: migrate
migrate:
	docker compose exec web python manage.py migrate

.PHONY: migrations
migrations:
	docker compose exec web python manage.py makemigrations

.PHONY: test
test:
	docker compose up -d
	docker compose exec web python manage.py collectstatic --noinput
	docker compose exec web pytest -v chipy_org/ -o cache_dir=/var/app/.my_cache_dir

.PHONY: format
format:
	docker compose exec web ruff check --fix .
	docker compose exec web ruff format .
	docker compose exec web isort .

.PHONY: format-check
format-check:
	docker compose exec web ruff check .
	docker compose exec web ruff format --check .
	docker compose exec web isort --check-only .

.PHONY: setup
setup: setup_env build

.PHONY: superuser
superuser:
	docker compose exec web ./manage.py createsuperuser

.PHONY: tail-logs
tail-logs:
	docker compose logs -f web

.PHONY: dev-data
dev-data:
	docker compose exec web python manage.py makedevdata
