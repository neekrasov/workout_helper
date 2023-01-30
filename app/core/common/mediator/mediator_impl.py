from typing import Any, Dict, Type

from .usecase import UseCase, Command
from .mediator_protocol import Mediator
from .exceptions import CommandNotFoundException


class MediatorImpl(Mediator):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Command], UseCase] = {}

    async def send(self, command: Command) -> Any:
        try:
            handler = self._handlers[type(command)]
        except KeyError:
            raise CommandNotFoundException(
                f"Command {command.__class__} not binded"
            )
        return await handler(command)

    def bind(self, command: Type[Command], usecase: UseCase):
        self._handlers[command] = usecase

    def send_sync(self, command: Command) -> Any:
        try:
            handler = self._handlers[type(command)]
        except KeyError:
            raise CommandNotFoundException(
                f"Command {command.__class__} not binded"
            )
        return handler(command)
