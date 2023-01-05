import abc
from typing import Any, TypeVar, Optional, Callable

from blacksheep.server.controllers import ApiController
from blacksheep.server.openapi.common import EndpointDocs
from blacksheep.server.openapi.v3 import OpenAPIHandler
from blacksheep.server.routing import RoutesRegistry


from app.settings import Settings

_HandlerType = TypeVar("_HandlerType", bound=Callable[..., Any])


class BaseController(ApiController):
    def __init__(
        self,
        router: RoutesRegistry,
        settings: Settings,
        docs: OpenAPIHandler,
    ) -> None:
        self._router = router
        self._settings = settings
        self._docs = docs

    @abc.abstractmethod
    def register(self) -> None:
        raise NotImplementedError()
        ...

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
