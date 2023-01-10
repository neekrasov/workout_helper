import http
from blacksheep import FromJSON

from app.core.common.base.result import TaskId
from app.core.workout.usecases.get_updates import GetUpdatesCommand
from app.core.workout.usecases.get_nearest_grounds import (
    GetNearestGroundCommand
)
from app.core.workout.exceptions.grounds import GroundsNotFoundException
from .base import BaseController
from ..models.grounds import CoordinatesGroundRequest


class GroundsController(BaseController):
    async def get_nearest(
        self,
        coordinates: FromJSON[CoordinatesGroundRequest],
    ):
        coordinates_value = coordinates.value
        try:
            result = await self._mediator.send(
                GetNearestGroundCommand(
                    latitude=coordinates_value.latitude,
                    longitude=coordinates_value.longitude,
                )
            )
        except GroundsNotFoundException:
            return self.pretty_json(
                status=http.HTTPStatus.NOT_FOUND,
                data={
                    "detail": "Grounds not found",
                },
            )
        return self.pretty_json(
            status=http.HTTPStatus.OK,
            data=result,
        )

    async def get_updates(
        self,
        task_id: str,
    ):
        result = await self._mediator.send(GetUpdatesCommand(TaskId(task_id)))
        return self.pretty_json(
            status=http.HTTPStatus.OK,
            data=result
        )

    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "grounds"

    def register(self) -> None:
        self.add_route(
            method="POST",
            path="/nearest",
            controller_method=self.get_nearest,
        )
        self.add_route(
            method="GET",
            path="/get-updates/{task_id}",
            controller_method=self.get_updates,
        )
