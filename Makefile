ifneq ($(wildcard deploy/.env),)
	ENV_FILE = .env
endif
ifneq ($(wildcard .env),)
	ifeq ($(DOCKER),)
		include .env
	endif
endif

export

update-dataset:
	poetry run python -m app.presentation.cli.update_dataset

run:
	make -j 3 run-api run-celery run-flower

run-api:
	poetry run gunicorn app.presentation.api.main:app --reload --bind $(HOST):$(BACKEND_PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--log-level ${APP_LOGGING_LEVEL} \
	--workers $(APP_WORKERS)

run-celery:
	poetry run celery -A app.presentation.celery.worker worker -l info

run-flower:
	poetry run celery -A app.presentation.celery.worker flower 

migrate-up:
	poetry run alembic -c deploy/alembic.ini upgrade head

migrate-down:
	poetry run alembic -c deploy/alembic.ini downgrade $(revision)

migrate-create:
	poetry run alembic -c deploy/alembic.ini revision --autogenerate -m $(name)

migrate-history:
	poetry run alembic -c deploy/alembic.ini history

migrate-stamp:
	poetry run alembic -c deploy/alembic.ini stamp $(revision)

run-tests:
	poetry run pytest -v

compose-build:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) build

compose-up:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) up -d

compose-logs:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) logs -f

compose-exec:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) exec backend bash

docker-rm-volume:
	docker volume rm -f workout_postgres_data

compose-down:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) down --remove-orphans

compose-update-dataset:
	docker exec -it workout_worker make update-dataset