from typing import Optional, cast

from blacksheep import Request
from guardpost.asynchronous.authentication import (
    BaseAuthenticationHandler,
    Identity
)
from app.core.user.usecases.auth import (
    GetCurrentUserUseCase,
)
from app.core.user.exceptions.auth import SessionNotFoundException


class AuthHandler(BaseAuthenticationHandler):
    def __init__(
        self,
        get_current_user_usecase: GetCurrentUserUseCase
    ):
        self._get_current_user_usecase = get_current_user_usecase

    async def authenticate(self, context: Request) -> Optional[Identity]:
        header_value = context.get_first_header(b"Authorization")
        if header_value:
            session_id = header_value.decode("utf-8")
            try:
                user = await self._get_current_user_usecase.execute(session_id)
                context.identity = cast(Identity, user)
            except SessionNotFoundException:
                context.identity = None
        else:
            context.identity = None
        return context.identity
