from typing import Callable
from celery import Celery

from app.settings import Settings
from .tasks import (
    get_nearest_grounds,
    search_grounds,
    get_recommendations,
)
from .factories import build_mediator


def build_celery() -> Celery:
    settings = Settings()
    app = Celery(
        "app",
        backend=settings.redis.redis_url,
        broker=settings.redis.redis_url,
    )
    mediator = build_mediator(settings)
    get_nearest_grounds_task = _inject_dependency_to_task(
        get_nearest_grounds, mediator=mediator
    )
    search_grounds_task = _inject_dependency_to_task(
        search_grounds, mediator=mediator
    )
    get_recommendations_task = _inject_dependency_to_task(
        get_recommendations, mediator=mediator
    )

    app.task(get_nearest_grounds_task, name="get_nearest_grounds")
    app.task(search_grounds_task, name="search_grounds")
    app.task(get_recommendations_task, name="get_recommendations")
    return app


def _inject_dependency_to_task(task: Callable, **depends) -> Callable:
    task_with_dependency = lambda *args: task(*args, **depends)  # noqa
    task_with_dependency.__name__ = task.__name__
    return task_with_dependency


app = build_celery()
