from typing import Callable
from celery import Celery

from app.settings import Settings
from app.core.common.mediator import MediatorImpl
from app.core.workout.usecases.calculate_nearest_grounds import (
    CalculateNearestGroundCommand,
    CalculateNearestGroundUseCase,
)
from .tasks import get_nearest_grounds


def build_celery() -> Celery:
    settings = Settings()
    app = Celery(
        "app",
        backend=settings.redis.redis_url,
        broker=settings.redis.redis_url,
    )
    mediator = build_mediator()
    task = _inject_dependency_to_task(get_nearest_grounds, mediator=mediator)
    app.task(task, name="get_nearest_grounds")
    return app


def _inject_dependency_to_task(task: Callable, **depends) -> Callable:
    task_with_dependency = lambda *args: task(*args, **depends)  # noqa
    task_with_dependency.__name__ = task.__name__
    return task_with_dependency


def build_mediator() -> MediatorImpl:
    mediator = MediatorImpl()
    mediator.bind(
        CalculateNearestGroundCommand, CalculateNearestGroundUseCase()
    )
    return mediator


app = build_celery()
