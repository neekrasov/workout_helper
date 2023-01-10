import contextlib
from typing import AsyncGenerator, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction
from sqlalchemy.exc import IntegrityError

from app.core.common.base.uow import UnitOfWork
from app.core.common.base.exceptions import UniqueConstraintViolation


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @contextlib.asynccontextmanager
    async def _transaction(self) -> AsyncGenerator:
        if not self._session.in_transaction() and self._session.is_active:
            async with self._session.begin() as transaction:
                yield transaction
        else:
            yield

    @property
    def pipeline(
        self,
    ) -> AsyncContextManager[AsyncSessionTransaction]:
        return self._transaction()

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise UniqueConstraintViolation()
