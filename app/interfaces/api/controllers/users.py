import http
from blacksheep import FromJSON
from app.core.user.usecases.auth_service import AuthUserService
from app.core.user.exceptions.users import UserAlreadyExistsException
from app.core.user.services.create_user import CreateUserCommand
from guardpost.authentication import User as GuardpostUser

from .base import BaseController
from ..models.user import UserCreateRequest


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
                    password=values.password,
                    email=values.email,
                )
            )
        except UserAlreadyExistsException:
            return self.pretty_json(
                status=http.HTTPStatus.CONFLICT,
                data={
                    "detail": "User already exists",
                },
            )
        return self.pretty_json(
            status=http.HTTPStatus.CREATED,
            data={
                "detail": "User created",
            },
        )

    async def get_current(self, user: GuardpostUser):
        if user is None:
            return self.pretty_json(
                status=http.HTTPStatus.UNAUTHORIZED,
                data={
                    "detail": "Not authenticated",
                },
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
        )
        self.add_route(
            method="GET",
            path="/me",
            controller_method=self.get_current,
        )
