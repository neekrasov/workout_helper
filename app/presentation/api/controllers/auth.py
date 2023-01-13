import http
import uuid
from blacksheep import FromForm, FromQuery
from blacksheep.server.openapi.common import (
    EndpointDocs,
    ResponseInfo,
    ContentInfo,
    ParameterInfo,
    RequestBodyInfo,
)

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
            doc=EndpointDocs(
                description="Login user",
                request_body=RequestBodyInfo(
                    description="Login form",
                ),
                responses={
                    401: ResponseInfo(strings.INVALID_CREDENTIALS),
                    200: ResponseInfo(
                        description="Session id",
                        content=[
                            ContentInfo(
                                type=dict,
                                examples=[
                                    {"session_id": "d42f838e-269e-4236-8b65-36e3df10b78b"}, # noqa
                                ],
                            )
                        ],
                    ),
                },
            ),
        )
        self.add_route(
            method="POST",
            path="/logout",
            controller_method=self.logout,
            doc=EndpointDocs(
                description="Logout user",
                parameters={
                    "session_id": ParameterInfo(
                        description="Session id",
                        example="d42f838e-269e-4236-8b65-36e3df10b78b",
                    )
                },
                responses={
                    404: ResponseInfo(strings.SESSION_NOT_FOUND),
                    202: ResponseInfo("User 35868fa8-e98a-48e8-9507-8c8422c957fd logged out"), # noqa
                },
            ),
        )
