import abc
from typing import Any, TypeVar, Optional, Callable
from blacksheep.server.controllers import ApiController
from blacksheep.server.openapi.common import EndpointDocs
from blacksheep.server.openapi.v3 import OpenAPIHandler
from blacksheep.server.routing import RoutesRegistry
from guardpost.authentication import User as GuardpostUser

from app.settings import Settings
from app.core.common.mediator import Mediator
from app.core.user.exceptions.auth import (
    InvalidTokenException,
)

_HandlerType = TypeVar("_HandlerType", bound=Callable[..., Any])


class BaseController(ApiController):
    def __init__(
        self,
        router: RoutesRegistry,
        settings: Settings,
        docs: OpenAPIHandler,
        mediator: Mediator,
    ) -> None:
        self._router = router
        self._settings = settings
        self._docs = docs
        self._mediator = mediator

    @abc.abstractmethod
    def register(self) -> None:
        raise NotImplementedError()

    def add_route(
        self,
        *decorators: Callable[[_HandlerType], _HandlerType],
        method: str,
        path: str,
        controller_method: _HandlerType,
        doc: Optional[EndpointDocs] = None,
    ) -> None:
        handler_func = controller_method.__func__  # type: ignore
        handler = self._mark_handler_as_method_of_controller(handler_func)
        if doc is not None:
            handler = self._docs(doc)(handler)

        for decorator in decorators:
            handler = decorator(handler)

        self._router.add(method, path, handler)

    def _mark_handler_as_method_of_controller(
        self, handler: _HandlerType
    ) -> _HandlerType:
        controller_type = self.__class__
        setattr(handler, "controller_type", controller_type)
        return handler

    def _check_user_auth(self, user: GuardpostUser):
        if not user:
            raise InvalidTokenException

    def _make_detail(self, detail: str) -> dict:
        return {"detail": detail}
