.PHONY: help

help:
	@echo "Type make, then hit tab to see make options"

run_db:
	docker-compose up -d db

setup_db:
	docker exec -it db psql -h db -U postgres -c "create database postgres;" >/dev/null || echo "[skipping] DB already setup"

setup_env:
	## Copy but don't overwrite the docker env
	cp -n docker/docker.env.sample docker/docker.env || true

build:
	docker-compose build

web:
	docker-compose up

migrate:
	docker exec -it web python manage.py migrate auth || true
	docker exec -it web python manage.py migrate

setup: setup_env build run_db setup_db
