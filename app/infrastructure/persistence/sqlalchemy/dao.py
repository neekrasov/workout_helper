from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base.dao import DAO


class DAOImpl(DAO):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
