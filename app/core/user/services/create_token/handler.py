from app.core.common.cqs import Handler

from .command import CreateTokenCommand
from ...usecases.auth_service import AuthUserService
from ...protocols.tokens_storage_dao import TokensStorageDAO


class CreateTokenHandler(Handler[CreateTokenCommand, None]):
    def __init__(
        self,
        auth_service: AuthUserService,
        tokens_dao: TokensStorageDAO,
    ) -> None:
        self._auth_service = auth_service
        self._tokens_dao = tokens_dao

    async def handle(self, event: CreateTokenCommand) -> None:
        token = self._auth_service.create_token(str(event.user_id))
        await self._tokens_dao.save(str(event.session_id), token)
