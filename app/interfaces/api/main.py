from blacksheep import Application, RoutesRegistry
from blacksheep.server.openapi.v3 import OpenAPIHandler

from app.settings import Settings
from app.core.common.base.uow import UnitOfWork
from app.core.common.cqs import MediatorProtocol
from app.infrastructure.persistence.sqlalchemy.models import start_mappers
from app.infrastructure.persistence.sqlalchemy.uow import UnitOfWorkImpl
from app.infrastructure.user.tokens_storage_dao import TokensStorageDAOImpl
from app.infrastructure.user.user_dao import (
    UserDAOWriterImpl,
    UserDAOReaderImpl,
)
# from app.core.user.usecases.user_service import UserService
from app.core.user.usecases.auth_service import AuthUserService
from app.core.user.protocols.tokens_storage_dao import TokensStorageDAO
from app.core.user.protocols.user_dao import UserDAOWriter, UserDAOReader
from app.core.user.usecases.auth import (
    GetCurrentUserUseCase,
    LoginUserUseCase,
    LogoutUserUseCase,
)


from .security.auth_handler import AuthHandler

from .factories.sqlalchemy import (
    sa_engine_factory,
    sa_sessionmaker_factory,
    sa_asyncsession_factory,
)

from .factories.base import (
    openapi_docs_factory,
    redis_client_factory,
    mediator_factory,
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
        self._app.services.add_scoped(GetCurrentUserUseCase)
        self._app.services.add_scoped(LoginUserUseCase)
        self._app.services.add_scoped(LogoutUserUseCase)

        # self._app.services.add_exact_scoped(UserService)
        self._app.services.add_exact_scoped(AuthUserService)

    def _setup_routes(self) -> None:
        docs = self._app.services.build_provider().get(OpenAPIHandler)
        mediator = self._app.services.build_provider().get(MediatorProtocol)
        controllers.setup(
            self._app.controllers_router, self._settings, docs, mediator
        )
        docs.bind_app(self._app)

    def _setup_security(self) -> None:
        get_current_user_usecase = self._app.services.build_provider().get(
            GetCurrentUserUseCase
        )
        self._app.use_authentication().add(
            AuthHandler(get_current_user_usecase)
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
