help: ## this help
	@echo "Makefile for managing application:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup_env: ## copy docker env from sample
	## Copy but don't overwrite the docker env
	[ -f docker/docker.env ] || cp docker/docker.env.sample docker/docker.env

build: ## build the application image
	docker compose build

run: ## run the application
	docker compose up

up: ## run the application in detached mode
	docker compose up -d

up-services: ## run the database in detached mode
	docker compose up -d db

down: ## stop the application
	docker compose down

shell: ## open a shell in the application container
	@echo "Opening shell in docker container"
	@echo "Use this shell to run python and django commands normally"
	@docker compose exec web bash

psql: ## open a psql shell in the database container
	@docker compose exec db psql chipy chipy

resetdb: ## reset the database
	@docker compose exec db psql chipy chipy -c "drop schema if exists public cascade;"
	@docker compose exec db psql chipy chipy -c "create schema public;"

web: run ## alias for run

migrate: ## run migrations
	docker compose exec web python manage.py migrate

migrations: ## create migrations
	docker compose exec web python manage.py makemigrations

test: ## run tests
	docker compose up -d
	docker compose exec web python manage.py collectstatic --noinput
	docker compose exec web pytest -v chipy_org/ -o cache_dir=/var/app/.my_cache_dir

format: ## format the code
	docker compose exec web ruff check --fix .
	docker compose exec web ruff format .
	docker compose exec web isort .

format-check: ## check the code formatting
	docker compose exec web ruff check .
	docker compose exec web ruff format --check .
	docker compose exec web isort --check-only .

setup: setup_env build ## setup the environment

superuser: ## create a superuser
	docker compose exec web ./manage.py createsuperuser

tail-logs: ## tail the application logs
	docker compose logs -f web

dev-data: ## create development data
	docker compose exec web python manage.py makedevdata
