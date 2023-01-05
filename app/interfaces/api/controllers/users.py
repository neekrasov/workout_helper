import http
from blacksheep import FromJSON
from app.core.user.dto.user import UserCreateDto
from app.core.user.usecases.auth_service import AuthUserService
from app.core.user.exceptions.users import UserAlreadyExistsException
from guardpost.authentication import User as GuardpostUser

from .base import BaseController


class UsersController(BaseController):
    async def create(
        self,
        user_data: FromJSON[UserCreateDto],
        auth_service: AuthUserService,
    ):
        try:
            await auth_service.create_user(user_data.value)
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
