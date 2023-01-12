import http
import uuid
from blacksheep import FromForm, FromQuery

from app.core.common.base.types import SessionId
from app.core.user.usecases.login_user import LoginUserCommand
from app.core.user.usecases.logout_user import LogoutUserCommand
from app.core.user.exceptions.auth import (
    SessionNotFoundException,
    InvalidCredentialsException,
)
from app.resources import strings
from .base import BaseController
from ..models.auth import LoginFormInputRequest


class AuthController(BaseController):
    async def login(
        self,
        form_data: FromForm[LoginFormInputRequest],
    ):
        form = form_data.value
        try:
            session_id = await self._mediator.send(
                LoginUserCommand(
                    form.username,
                    form.password,
                )
            )
        except InvalidCredentialsException:
            return self.pretty_json(
                status=http.HTTPStatus.UNAUTHORIZED,
                data=self._make_detail(strings.INVALID_CREDENTIALS),
            )
        return self.json({"session_id": session_id})

    async def logout(
        self,
        session_id: FromQuery[uuid.UUID],
    ):
        try:
            user_id = await self._mediator.send(
                LogoutUserCommand(SessionId(session_id.value))
            )
        except SessionNotFoundException:
            return self.pretty_json(
                status=http.HTTPStatus.NOT_FOUND,
                data=self._make_detail(strings.SESSION_NOT_FOUND),
            )
        return self.pretty_json(
            status=http.HTTPStatus.ACCEPTED,
            data=self._make_detail(f"User {user_id} logged out"),
        )

    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "auth"

    def register(self) -> None:
        self.add_route(
            method="POST",
            path="/login",
            controller_method=self.login,
        )
        self.add_route(
            method="POST",
            path="/logout",
            controller_method=self.logout,
        )
