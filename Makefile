.PHONY: help

help:
	@echo "Type make, then hit tab to see make options"

setup_env:
	## Copy but don't overwrite the docker env
	cp -n docker/docker.env.sample docker/docker.env || true

build:
	docker-compose build

run:
	docker-compose up -d

web: run

up: run

down:
	docker-compose down

migrate:
	docker-compose exec web python manage.py migrate auth || true
	docker-compose exec web python manage.py migrate

datamigration:
	docker-compose exec web python manage.py makemigrations --name $(name) --empty $(app)

migration:
	docker-compose exec web python manage.py makemigrations --name $(name) $(app)

setup: setup_env build run migrate
