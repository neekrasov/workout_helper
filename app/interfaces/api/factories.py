from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from rodi import GetServiceContext
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from app.settings import Settings


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


def sa_engine_factory(services: GetServiceContext) -> AsyncEngine:
    settings = services.provider.get(Settings)
    engine: AsyncEngine = create_async_engine(
        settings.postgres.postgres_url, echo=True
    )
    return engine


def sa_sessionmaker_factory(services: GetServiceContext) -> sessionmaker:
    engine = services.provider.get(AsyncEngine)
    return sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )


def sa_asyncsession_factory(services: GetServiceContext) -> AsyncSession:
    sessionmaker_ = services.provider.get(sessionmaker)
    return sessionmaker_()


def redis_client_factory(services: GetServiceContext) -> Redis:
    settings = services.provider.get(Settings)
    return Redis.from_url(settings.redis.redis_url, decode_responses=True)
