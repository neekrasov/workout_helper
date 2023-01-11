import http
import uuid
from dataclasses import asdict
from blacksheep import FromJSON, FromQuery
from guardpost.authentication import User as GuardpostUser

from app.core.common.base.result import TaskId
from app.core.common.base.types import UserId, GroundId
from app.core.workout.exceptions.grounds import GroundsNotFoundException
from app.core.workout.usecases.get_updates import GetUpdatesCommand
from app.core.workout.usecases.nearest_grounds import (
    GetNearestGroundCommand,
)
from app.core.workout.usecases.search_grounds import SearchGroundsCommand
from .base import BaseController
from ..models.grounds import (
    CoordinatesGroundRequest,
    SearchGroundsRequest,
)
from app.core.workout.usecases.like_ground import LikeGroundCommand


class GroundsController(BaseController):
    async def get_nearest(
        self,
        coordinates: FromJSON[CoordinatesGroundRequest],
        count: FromQuery[int],
    ):
        coordinates_value = coordinates.value
        try:
            result = await self._mediator.send(
                GetNearestGroundCommand(
                    latitude=coordinates_value.latitude,
                    longitude=coordinates_value.longitude,
                    count=count.value,
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

    async def search_grounds(
        self, query: FromJSON[SearchGroundsRequest], count: FromQuery[int]
    ):
        result = await self._mediator.send(
            SearchGroundsCommand(
                search_params=asdict(query.value),
                count=count.value,
            )
        )
        return self.pretty_json(
            status=http.HTTPStatus.OK,
            data=result,
        )

    async def like_ground(self, ground_id: int, user: GuardpostUser):
        if not user:
            return self.pretty_json(
                status=http.HTTPStatus.UNAUTHORIZED,
                data={
                    "detail": "User is not authorized",
                }
            )
        try:
            await self._mediator.send(
                LikeGroundCommand(
                    ground_id=GroundId(ground_id),
                    user_id=UserId(uuid.UUID(str(user.id))),
                )
            )
        except GroundsNotFoundException:
            return self.pretty_json(
                status=http.HTTPStatus.NOT_FOUND,
                data={
                    "detail": "Grounds not found",
                }
            )
        return self.pretty_json(
            status=http.HTTPStatus.OK,
            data={
                "detail": f"Ground liked by user {user.id}",
            },
        )

    async def get_updates(
        self,
        task_id: str,
    ):
        result = await self._mediator.send(GetUpdatesCommand(TaskId(task_id)))
        return self.pretty_json(status=http.HTTPStatus.OK, data=result)

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
        self.add_route(
            method="POST",
            path="/search",
            controller_method=self.search_grounds,
        )
        self.add_route(
            method="POST",
            path="/like",
            controller_method=self.like_ground,
        )
