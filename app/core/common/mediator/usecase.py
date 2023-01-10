from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .command import Command

CommandType = TypeVar("CommandType", bound=Command)
ReturnType = TypeVar("ReturnType")


class UseCase(ABC, Generic[CommandType, ReturnType]):
    @abstractmethod
    async def handle(self, command: CommandType) -> ReturnType:
        ...

    async def __call__(self, *args, **kwargs) -> ReturnType:
        return await self.handle(*args, **kwargs)
