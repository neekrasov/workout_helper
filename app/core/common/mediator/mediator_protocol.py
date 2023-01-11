from typing import Protocol, Any, Type

from .command import Command
from .usecase import UseCase


class Mediator(Protocol):
    async def send(self, command: Command):
        ...

    def bind(
        self,
        event: Type[Command],
        handler: UseCase[Command, Any],
    ):
        ...

    def send_sync(self, command: Command):
        ...
