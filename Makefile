ifneq ($(wildcard .env),)
	include .env
endif

export

update-dataset:
	poetry run python -m app.presentation.cli.update_dataset

run:
	make -j 3 run-api run-celery run-flower

run-api:
	poetry run uvicorn app.presentation.api.main:app --reload

run-celery:
	poetry run celery -A app.presentation.celery.worker worker -l info

run-flower:
	poetry run celery -A app.presentation.celery.worker flower 

migrate-up:
	poetry run alembic -c ./app/infrastructure/persistence/sqlalchemy/alembic.ini upgrade head

migrate-down:
	poetry run alembic -c ./app/infrastructure/persistence/sqlalchemy/alembic.ini downgrade $(revision)

migrate-create:
	poetry run alembic -c ./app/infrastructure/persistence/sqlalchemy/alembic.ini revision --autogenerate -m $(name)

migrate-history:
	poetry run alembic -c ./app/infrastructure/persistence/sqlalchemy/alembic.ini history

migrate-stamp:
	poetry run alembic -c ./app/infrastructure/persistence/sqlalchemy/alembic.ini stamp $(revision)