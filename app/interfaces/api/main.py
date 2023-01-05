from blacksheep import Application, RoutesRegistry
from blacksheep.server.openapi.v3 import OpenAPIHandler

from app.settings import Settings
from app.core.user.usecases.auth_service import AuthUserService
from app.core.user.usecases.user_service import UserService
from app.core.user.protocols.tokens_storage_dao import TokensStorageDAO
from app.core.user.protocols.user_dao import UserDAOWriter, UserDAOReader

from app.infrastructure.user.tokens_storage_dao import TokensStorageDAOImpl
from app.infrastructure.user.user_dao import (
    UserDAOWriterImpl,
    UserDAOReaderImpl,
)

from app.infrastructure.persistence.sqlalchemy.models import start_mappers
from app.core.common.uow import UnitOfWork
from app.infrastructure.persistence.sqlalchemy.uow import UnitOfWorkImpl

from .security.auth_handler import AuthHandler

from .factories import (
    openapi_docs_factory,
    sa_engine_factory,
    sa_sessionmaker_factory,
    redis_client_factory,
    sa_asyncsession_factory,
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

        # Databases
        self._app.services.add_scoped_by_factory(sa_engine_factory)
        self._app.services.add_scoped_by_factory(sa_sessionmaker_factory)
        self._app.services.add_scoped_by_factory(sa_asyncsession_factory)
        self._app.services.add_scoped_by_factory(redis_client_factory)
        self._app.services.add_scoped(UnitOfWork, UnitOfWorkImpl)

        # Auth and users
        self._app.services.add_scoped(UserDAOReader, UserDAOReaderImpl)
        self._app.services.add_scoped(UserDAOWriter, UserDAOWriterImpl)
        self._app.services.add_scoped(TokensStorageDAO, TokensStorageDAOImpl)

        self._app.services.add_exact_scoped(UserService)
        self._app.services.add_exact_scoped(AuthUserService)

    def _setup_routes(self) -> None:
        docs = self._app.services.build_provider().get(OpenAPIHandler)
        controllers.setup(self._app.controllers_router, self._settings, docs)
        docs.bind_app(self._app)

    def _setup_security(self) -> None:
        auth_service = self._app.services.build_provider().get(AuthUserService)
        self._app.use_authentication().add(AuthHandler(auth_service))

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
