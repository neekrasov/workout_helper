import http
import uuid
from dataclasses import asdict
from blacksheep import FromJSON, FromQuery
from guardpost.authentication import User as GuardpostUser

from app.core.common.base.result import TaskId
from app.core.common.base.types import UserId, GroundId
from app.core.workout.exceptions.grounds import (
    GroundsNotFoundException,
    UserDoesNotLikeGroundException,
    UserAlreadyLikedGroundException,
)
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
from app.core.workout.usecases.recommendations import GetRecommendationsCommand
from app.core.workout.usecases.delete_like_ground import (
    DeleteLikeGroundCommand,
)
from app.resources import strings


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
                data=self._make_detail(strings.GROUNDS_NOT_FOUND),
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
        self._check_user_auth(user)
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
                data=self._make_detail(strings.GROUNDS_NOT_FOUND),
            )
        except UserAlreadyLikedGroundException:
            return self.pretty_json(
                status=http.HTTPStatus.CONFLICT,
                data=self._make_detail(strings.USER_ALREADY_LIKED_GROUND),
            )
        return self.pretty_json(
            status=http.HTTPStatus.OK,
            data=self._make_detail(f"Ground liked by user {user.id}"),
        )

    async def delete_like_ground(self, ground_id: int, user: GuardpostUser):
        self._check_user_auth(user)
        try:
            await self._mediator.send(
                DeleteLikeGroundCommand(
                    ground_id=GroundId(ground_id),
                    user_id=UserId(uuid.UUID(str(user.id))),
                )
            )
        except UserDoesNotLikeGroundException:
            return self.pretty_json(
                status=http.HTTPStatus.NOT_FOUND,
                data=self._make_detail(strings.USER_DOES_NOT_LIKE_GROUND),
            )
        return self.pretty_json(
            status=http.HTTPStatus.OK,
            data=self._make_detail(f"Ground unliked by user {user.id}"),
        )

    async def get_recommendations(
        self,
        ground_id: FromQuery[int],
        user: GuardpostUser,
        count: FromQuery[int],
    ):
        self._check_user_auth(user)
        try:
            result = await self._mediator.send(
                GetRecommendationsCommand(
                    ground_id=GroundId(ground_id.value),
                    user_id=UserId(uuid.UUID(str(user.id))),
                    count=count.value,
                )
            )
        except UserDoesNotLikeGroundException:
            return self.pretty_json(
                status=http.HTTPStatus.NOT_FOUND,
                data=self._make_detail(strings.USER_DOES_NOT_LIKE_GROUND),
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
        self.add_route(
            method="GET",
            path="/recommendations",
            controller_method=self.get_recommendations,
        )
