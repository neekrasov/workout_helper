from typing import Protocol, AsyncContextManager


class UnitOfWork(Protocol):
    @property
    def pipeline(self) -> AsyncContextManager:
        ...
