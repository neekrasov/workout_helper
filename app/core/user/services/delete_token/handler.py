from app.core.common.cqs import Handler

from .command import DeleteTokenCommand
from ...protocols.tokens_storage_dao import TokensStorageDAO


class DeleteTokenHandler(Handler[DeleteTokenCommand, None]):
    def __init__(
        self,
        tokens_dao: TokensStorageDAO,
    ) -> None:
        self._tokens_dao = tokens_dao

    async def handle(self, event: DeleteTokenCommand) -> None:
        await self._tokens_dao.delete_token(str(event.session_id))
