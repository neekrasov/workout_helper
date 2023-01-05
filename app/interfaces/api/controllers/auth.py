import http
from blacksheep import FromForm, FromQuery

from app.core.user.usecases.auth_service import AuthUserService
from app.core.user.exceptions.auth import (
    SessionNotFoundException,
    InvalidCredentialsException,
)
from .base import BaseController
from ..models.auth import LoginFormInputRequest


class AuthController(BaseController):

    async def login(
        self,
        form_data: FromForm[LoginFormInputRequest],
        auth_service: AuthUserService
    ):
        form = form_data.value
        try:
            session_id = await auth_service.login(
                email=form.username, raw_password=form.password
            )
        except InvalidCredentialsException:
            return self.pretty_json(
                status=http.HTTPStatus.UNAUTHORIZED,
                data={
                    "detail": "Invalid credentials"
                }
            )
        return self.json({"session_id": session_id})

    async def logout(
        self,
        session_id: FromQuery[str],
        auth_service: AuthUserService
    ):
        try:
            user_id = await auth_service.logout(session_id.value)
        except SessionNotFoundException:
            return self.pretty_json(
                status=http.HTTPStatus.NOT_FOUND,
                data={
                    "detail": "Session not found"
                }
            )
        return self.pretty_json(
                status=http.HTTPStatus.ACCEPTED,
                data={
                    "detail": f"User {user_id} logged out"
                }
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
