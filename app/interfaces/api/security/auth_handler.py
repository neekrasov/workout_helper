import uuid
from typing import Optional, cast
from blacksheep import Request
from guardpost.asynchronous.authentication import (
    BaseAuthenticationHandler,
    Identity
)

from app.core.common.mediator import Mediator
from app.core.user.usecases.get_current_user import (
    GetCurrentUserCommand,
)
from app.core.user.protocols.token_gateway import SessionId
from app.core.user.exceptions.auth import SessionNotFoundException


class AuthHandler(BaseAuthenticationHandler):
    def __init__(
        self,
        mediator: Mediator
    ):
        self._mediator = mediator

    async def authenticate(self, context: Request) -> Optional[Identity]:
        header_value = context.get_first_header(b"Authorization")
        if header_value:
            session_id = header_value.decode("utf-8")
            try:
                user = await self._mediator.send(
                    GetCurrentUserCommand(
                        SessionId(uuid.UUID(session_id))
                    )
                )
                context.identity = cast(Identity, user)
            except SessionNotFoundException:
                context.identity = None
        else:
            context.identity = None
        return context.identity
