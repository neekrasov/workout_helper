from abc import ABC, abstractmethod
from typing import Generic, TypeVar

EventType = TypeVar("EventType")
ReturnType = TypeVar("ReturnType")


class Handler(ABC, Generic[EventType, ReturnType]):
    @abstractmethod
    async def handle(self, event: EventType) -> ReturnType:
        ...

    async def __call__(self, *args, **kwargs) -> ReturnType:
        return await self.handle(*args, **kwargs)
