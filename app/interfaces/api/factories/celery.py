from rodi import GetServiceContext
from celery import Celery

from app.settings import Settings


def celery_factory(services: GetServiceContext) -> Celery:
    settings = services.provider.get(Settings)
    celery = Celery(
        "app",
        backend=settings.redis.redis_url,
        broker=settings.redis.redis_url,
    )
    return celery
