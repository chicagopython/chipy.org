help:
	@echo "Type make, then hit tab to see make options"

setup_env:
	## Copy but don't overwrite the docker env
	cp --update=none docker/docker.env.sample docker/docker.env || true

build:
	docker compose build

run:
	docker compose up

up:
	docker compose up -d

up-services:
	docker compose up -d db

down:
	docker compose down

shell:
	@echo "Opening shell in docker container"
	@echo "Use this shell to run python and django commands normally"
	@docker compose exec web bash

psql:
	@docker compose exec db psql chipy chipy

resetdb:
	@docker compose exec db psql chipy chipy -c "drop schema if exists public cascade;"
	@docker compose exec db psql chipy chipy -c "create schema public;"

web: run

migrate:
	docker compose exec web python manage.py migrate

migrations:
	docker compose exec web python manage.py makemigrations

test:
	docker compose up -d
	docker compose exec web python manage.py collectstatic --noinput
	docker compose exec web pytest -v chipy_org/ -o cache_dir=/var/app/.my_cache_dir

format:
	docker compose exec web ruff check --fix .
	docker compose exec web ruff format .
	docker compose exec web isort .

format-check:
	docker compose exec web ruff check .
	docker compose exec web ruff format --check .
	docker compose exec web isort --check-only .

setup: setup_env build

superuser:
	docker compose exec web ./manage.py createsuperuser

tail-logs:
	docker compose logs -f web

dev-data:
	docker compose exec web python manage.py makedevdata
