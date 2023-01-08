from blacksheep import RoutesRegistry
from blacksheep.server.openapi.v3 import OpenAPIHandler

from app.settings import Settings
from app.core.common.cqs import MediatorProtocol
from .base import BaseController
from .info import InfoController
from .auth import AuthController
from .users import UsersController


def setup(
    route_registry: RoutesRegistry,
    settings: Settings,
    docs: OpenAPIHandler,
    mediator: MediatorProtocol,
) -> None:

    controllers: list[BaseController] = [
        InfoController(
            router=route_registry,
            settings=settings,
            docs=docs,
            mediator=mediator,
        ),
        AuthController(
            router=route_registry,
            settings=settings,
            docs=docs,
            mediator=mediator,
        ),
        UsersController(
            router=route_registry,
            settings=settings,
            docs=docs,
            mediator=mediator,
        )
    ]
    for controller in controllers:
        controller.register()
