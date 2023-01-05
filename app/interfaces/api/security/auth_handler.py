from typing import Optional, cast

from blacksheep import Request
from guardpost.asynchronous.authentication import (
    BaseAuthenticationHandler,
    Identity
)

from app.core.user.usecases.auth_service import AuthUserService


class AuthHandler(BaseAuthenticationHandler):
    def __init__(self, auth_service: AuthUserService):
        self._auth_service = auth_service

    async def authenticate(self, context: Request) -> Optional[Identity]:
        header_value = context.get_first_header(b"Authorization")
        if header_value:
            value = header_value.decode("utf-8")
            user = await self._auth_service.get_current_user(value)
            context.identity = cast(Identity, user)
        else:
            context.identity = None
        return context.identity
