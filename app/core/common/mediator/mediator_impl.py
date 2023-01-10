from typing import Any, Dict, Type

from .usecase import UseCase, Command
from .mediator_protocol import Mediator
from .exceptions import CommandNotFoundException


class MediatorImpl(Mediator):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Command], UseCase] = {}

    async def send(self, command: Command) -> Any:
        handler = self._handlers[type(command)]
        if handler is None:
            raise CommandNotFoundException(command)
        return await handler(command)

    def bind(self, command: Type[Command], handler: UseCase):
        self._handlers[command] = handler

    def send_sync(self, command: Command) -> Any:
        handler = self._handlers[type(command)]
        if handler is None:
            raise CommandNotFoundException(command)
        return handler(command)
