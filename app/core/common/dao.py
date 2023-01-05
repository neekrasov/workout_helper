from typing import Protocol


class DAOWriter(Protocol):
    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...


class DAO(Protocol):
    ...
