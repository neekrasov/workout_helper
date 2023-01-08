from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from rodi import GetServiceContext
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from app.settings import Settings
from app.core.common.cqs import MediatorImpl, MediatorProtocol
from app.infrastructure.persistence.sqlalchemy.uow import UnitOfWorkImpl

from .user_mediator import user_mediator_bind


def openapi_docs_factory(services: GetServiceContext) -> OpenAPIHandler:
    settings = services.provider.get(Settings)
    return OpenAPIHandler(
        info=Info(
            title=settings.title,
            description=settings.description,
            version=settings.version,
        ),
        ui_path="/api/docs",
        json_spec_path="/api/spec.json",
    )


def redis_client_factory(services: GetServiceContext) -> Redis:
    settings = services.provider.get(Settings)
    return Redis.from_url(settings.redis.redis_url, decode_responses=True)


def mediator_factory(services: GetServiceContext) -> MediatorProtocol:
    mediator = MediatorImpl()

    session = services.provider.get(AsyncSession)
    uow = UnitOfWorkImpl(session)
    redis = services.provider.get(Redis)

    mediator = user_mediator_bind(mediator, session, uow, redis, services)

    return mediator
