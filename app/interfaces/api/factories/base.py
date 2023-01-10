from redis.asyncio import Redis
from rodi import GetServiceContext
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from app.core.user.services.auth_service import AuthUserService
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


def redis_client_factory(services: GetServiceContext) -> Redis:
    settings = services.provider.get(Settings)
    return Redis.from_url(settings.redis.redis_url, decode_responses=True)


def auth_user_service_factory(services: GetServiceContext) -> AuthUserService:
    settings: Settings = services.provider.get(Settings)
    return AuthUserService(
        secret_key=settings.secret_key,
        token_expiration=settings.token_expiration,
    )
