from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.dao import DAO, DAOWriter


class DAOImpl(DAO):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session


class DAOWriterImpl(DAOWriter, DAOImpl):
    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
