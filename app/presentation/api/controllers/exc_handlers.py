import http
from blacksheep import Request, json

from app.core.common.base.exceptions import ValidationError


async def validation_error_handler(
    self, request: Request, exc: ValidationError
):
    return json(
        status=http.HTTPStatus.FORBIDDEN,
        data={
            "detail": exc.detail,
        },
    )
