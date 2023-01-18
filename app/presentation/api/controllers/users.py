import http
from blacksheep import FromJSON
from guardpost.authentication import User as GuardpostUser
from blacksheep.server.openapi.common import (
    EndpointDocs,
    ResponseInfo,
    ContentInfo,
)
from app.core.user.entities.user import User
from app.core.user.services.auth_service import AuthUserService
from app.core.user.exceptions.users import UserAlreadyExistsException
from app.core.user.usecases.create_user import CreateUserCommand
from .base import BaseController
from ..models.user import UserCreateRequest
from app.resources import strings


class UsersController(BaseController):
    async def create(
        self,
        user_data: FromJSON[UserCreateRequest],
        auth_service: AuthUserService,
    ):
        values = user_data.value
        try:
            await self._mediator.send(
                CreateUserCommand(
                    username=values.username,
                    raw_password=values.password,
                    email=values.email,
                )
            )
        except UserAlreadyExistsException:
            return self.pretty_json(
                status=http.HTTPStatus.BAD_REQUEST,
                data=self._make_detail(strings.USER_AREADY_EXISTS),
            )
        return self.pretty_json(
            status=http.HTTPStatus.CREATED,
            data=self._make_detail(strings.USER_CREATED),
        )

    async def get_current(self, user: GuardpostUser):
        if user is None:
            return self.pretty_json(
                status=http.HTTPStatus.UNAUTHORIZED,
                data=self._make_detail(strings.NOT_AUTHENTICATED),
            )
        return self.pretty_json(
            status=http.HTTPStatus.OK,
            data=user,
        )

    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "users"

    def register(self) -> None:
        self.add_route(
            method="POST",
            path="/",
            controller_method=self.create,
            doc=EndpointDocs(
                description="Create a new user",
                responses={
                    201: ResponseInfo(strings.USER_CREATED),
                    409: ResponseInfo(strings.USER_AREADY_EXISTS),
                },
            ),
        )
        self.add_route(
            method="GET",
            path="/me",
            controller_method=self.get_current,
            doc=EndpointDocs(
                description="Get current user",
                responses={
                    200: ResponseInfo(
                        description="Current user",
                        content=[
                            ContentInfo(
                                type=User
                            )
                        ]
                    )
                }
            )
        )
