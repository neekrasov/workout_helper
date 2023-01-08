from typing import Protocol, Union, Any, Type

from ..command import Command
from ..query import Query
from ..handler import Handler

Event = Union[Command, Query]


class MediatorProtocol(Protocol):
    async def send(self, event: Event):
        ...

    def bind(
        self,
        event: Type[Event],
        handler: Handler[Event, Any],
    ):
        ...
