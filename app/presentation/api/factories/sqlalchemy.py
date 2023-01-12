from rodi import GetServiceContext
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.settings import Settings


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
