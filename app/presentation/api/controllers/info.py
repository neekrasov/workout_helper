from blacksheep import json

from app.settings import Settings
from .base import BaseController


class InfoController(BaseController):
    async def info(self, settings: Settings):

        return json(
            {
                "title": settings.title,
                "description": settings.description,
                "version": settings.version,
                "debug": settings.debug,
                "erorr_details": settings.show_error_details,

            }
        )

    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "info"

    def register(self) -> None:
        self.add_route(
            method="GET",
            path="/",
            controller_method=self.info,
        )
