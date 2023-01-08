from typing import Optional
from app.core.common.cqs import Handler

from .query import GetTokenQuery
from ...usecases.auth_service import AuthUserService
from ...protocols.tokens_storage_dao import TokensStorageDAO


class GetTokenHandler(Handler[GetTokenQuery, Optional[str]]):
    def __init__(
        self,
        auth_service: AuthUserService,
        tokens_dao: TokensStorageDAO,
    ) -> None:
        self._auth_service = auth_service
        self._tokens_dao = tokens_dao

    async def handle(self, event: GetTokenQuery) -> Optional[str]:
        token = await self._tokens_dao.get_token(str(event.session_id))
        return token
