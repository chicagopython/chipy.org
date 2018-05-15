run_db:
	docker-compose up -d chipy-db

setup_db:
	docker exec -it chipy-db psql -h chipy-db -U postgres -c "create database chipy;" >/dev/null || echo "[skipping] DB already setup"

setup_env:
	## Copy but don't overwrite the docker env
	cp -n docker/docker.env.sample docker/docker.env || true

build:
	docker-compose build

web:
	docker-compose up chipy-db chipy-web

migrate:
	docker exec -it chipy-web python manage.py migrate auth || true
	docker exec -it chipy-web python manage.py migrate

setup: setup_env build run_db setup_db
