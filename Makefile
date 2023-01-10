ifneq ($(wildcard .env),)
	include .env
endif

export

run:
	make -j 2 run-api run-celery

run-api:
	poetry run uvicorn app.interfaces.api.main:app --reload

run-celery:
	poetry run celery -A app.interfaces.celery.worker worker -l info

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