from blacksheep import Application, RoutesRegistry
from blacksheep.server.openapi.v3 import OpenAPIHandler

from app.settings import Settings
from app.core.common.base.uow import UnitOfWork
from app.core.common.mediator import Mediator
from app.infrastructure.persistence.sqlalchemy.mapping import start_mappers
from app.infrastructure.persistence.sqlalchemy.uow import UnitOfWorkImpl
from app.infrastructure.persistence.redis.token_gateway import TokenGatewayImpl
from app.infrastructure.persistence.sqlalchemy.gateways import (
    UserWriteGatewayImpl,
    UserReadGatewayImpl,
)
from app.core.user.protocols.token_gateway import TokenGateway
from app.core.user.protocols.user_gateway import (
    UserWriteGateway,
    UserReadGateway
)
from app.core.workout.protocols.analysis import AnalysisSportsGround
from app.infrastructure.worker.analysis import AnalysisSportsGroundImpl
from .factories.mediator import mediator_factory
from .security.auth_handler import AuthHandler
from .factories.celery import celery_factory
from .factories.sqlalchemy import (
    sa_engine_factory,
    sa_sessionmaker_factory,
    sa_asyncsession_factory,
)
from .factories.base import (
    openapi_docs_factory,
    redis_client_factory,
    auth_user_service_factory,
)
from . import controllers


class ApplicationBuilder:
    def __init__(self, settings: Settings):
        self._routes_registry = RoutesRegistry()
        self._app = Application(
            debug=settings.debug,
            show_error_details=settings.show_error_details,
        )
        self._app.controllers_router = self._routes_registry
        self._settings = settings

    def _setup_di(self):
        self._app.services.add_instance(self._routes_registry, RoutesRegistry)
        self._app.services.add_exact_transient(Settings)
        self._app.services.add_singleton_by_factory(openapi_docs_factory)
        self._app.services.add_scoped_by_factory(mediator_factory)
        self._app.services.add_scoped_by_factory(celery_factory)

        # Databases
        self._app.services.add_scoped_by_factory(sa_engine_factory)
        self._app.services.add_scoped_by_factory(sa_sessionmaker_factory)
        self._app.services.add_scoped_by_factory(sa_asyncsession_factory)
        self._app.services.add_scoped_by_factory(redis_client_factory)
        self._app.services.add_scoped(UnitOfWork, UnitOfWorkImpl)

        # Auth and users
        self._app.services.add_scoped_by_factory(auth_user_service_factory)
        self._app.services.add_scoped(UserReadGateway, UserReadGatewayImpl)
        self._app.services.add_scoped(UserWriteGateway, UserWriteGatewayImpl)
        self._app.services.add_scoped(TokenGateway, TokenGatewayImpl)

        # Workout
        self._app.services.add_scoped(
            AnalysisSportsGround, AnalysisSportsGroundImpl
        )

    def _setup_routes(self) -> None:
        docs = self._app.services.build_provider().get(OpenAPIHandler)
        mediator = self._app.services.build_provider().get(Mediator)
        controllers.setup(
            self._app.controllers_router, self._settings, docs, mediator
        )
        docs.bind_app(self._app)

    def _setup_security(self) -> None:
        mediator = self._app.services.build_provider().get(
            Mediator
        )
        self._app.use_authentication().add(
            AuthHandler(mediator)
        )

    def build(self) -> Application:
        start_mappers()
        self._setup_di()
        self._setup_routes()
        self._setup_security()
        return self._app


def create_app() -> Application:
    builder = ApplicationBuilder(Settings())
    return builder.build()


app = create_app()
