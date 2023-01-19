import http
from typing import Union
from blacksheep import Request, json

from app.core.common.base.exceptions import ValidationError
from app.core.user.exceptions.auth import (
    SessionNotFoundException,
    InvalidCredentialsException,
    InvalidTokenException,
)


async def validation_error_handler(
    self, request: Request, exc: ValidationError
):
    return json(
        status=http.HTTPStatus.FORBIDDEN,
        data={
            "detail": exc.detail,
        },
    )


AuthExceptionType = Union[
    SessionNotFoundException,
    InvalidCredentialsException,
    InvalidTokenException,
]


async def auth_error_handler(self, request: Request, exc: AuthExceptionType):
    return json(
        status=http.HTTPStatus.UNAUTHORIZED,
        data={
            "detail": "User is not authorized",
        },
    )
