from typing import Any, Dict, Type

from ..handler import Handler
from .protocol import Event, MediatorProtocol
from ..exceptions import EventNotFoundException


class MediatorImpl(MediatorProtocol):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Event], Handler] = {}

    async def send(self, event: Event) -> Any:
        handler = self._handlers[type(event)]
        if handler is None:
            raise EventNotFoundException(event)
        return await handler(event)

    def bind(self, event: Type[Event], handler: Handler):
        self._handlers[event] = handler
