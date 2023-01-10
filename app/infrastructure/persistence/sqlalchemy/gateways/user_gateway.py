from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.user.protocols import UserReadGateway, UserWriteGateway
from app.core.user.entities import User, UserId

from ..gateway import BaseGateway


class UserReadGatewayImpl(BaseGateway, UserReadGateway):
    async def get_user_by_id(self, user_id: UserId) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalars().first()


class UserWriteGatewayImpl(BaseGateway, UserWriteGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def create_user(self, user: User) -> None:
        user.id = user.generate_id()
        self._session.add(user)
