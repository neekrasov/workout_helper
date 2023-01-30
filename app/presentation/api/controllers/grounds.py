import http
import uuid
from typing import List
from dataclasses import asdict
from blacksheep import FromJSON, FromQuery
from guardpost.authentication import User as GuardpostUser
from blacksheep.server.openapi.common import (
    EndpointDocs,
    ResponseInfo,
    ContentInfo,
    ParameterInfo,
)

from app.core.common.base.result import (
    TaskId,
    CalculationResult,
    ResultStatus,
    ResultType,
)
from app.core.common.base.types import UserId, GroundId
from app.core.workout.entities.sports_ground import (
    SportsGround,
    Location,
    Contact,
    Conditions,
)
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
from app.core.workout.usecases.like_ground import LikeGroundCommand
from app.core.workout.usecases.recommendations import GetRecommendationsCommand
from app.core.workout.usecases.delete_like_ground import (
    DeleteLikeGroundCommand,
)
from app.core.workout.usecases.user_grounds import GetUserGroundsCommand
from app.resources import strings
from .base import BaseController
from ..models.grounds import SearchGroundsRequest


class GroundsController(BaseController):
    async def get_nearest(
        self,
        latitude: FromQuery[float],
        longitude: FromQuery[float],
        count: FromQuery[int],
    ):
        result = await self._mediator.send(
            GetNearestGroundCommand(
                latitude=latitude.value,
                longitude=longitude.value,
                count=count.value,
            )
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
                status=http.HTTPStatus.BAD_REQUEST,
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

    async def get_user_grounds(self, user: GuardpostUser):
        self._check_user_auth(user)
        try:
            result = await self._mediator.send(
                GetUserGroundsCommand(
                    user_id=UserId(uuid.UUID(str(user.id))),
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
            method="GET",
            path="/nearest",
            controller_method=self.get_nearest,
            doc=EndpointDocs(
                description=(
                    "Get the nearest sports grounds by latitude and longitude."
                ),
                parameters={
                    "latitude": ParameterInfo(
                        description="Latitude of the point.",
                        example="55.753215",
                    ),
                    "longitude": ParameterInfo(
                        description="Longitude of the point.",
                        example="37.622504",
                    ),
                    "count": ParameterInfo(
                        description="Number of grounds to return.",
                        example="5",
                    ),
                },
                responses={
                    200: ResponseInfo(
                        description="Task ID to get updates.",
                        content=[
                            ContentInfo(
                                type=CalculationResult[TaskId],
                                examples=[
                                    CalculationResult(
                                        type=ResultType.ID,
                                        status=ResultStatus.SUCCESS,
                                        data=TaskId("92a877b1-b657-4d0e-a749-9f4f244fdca2"), # noqa,
                                    ),
                                ],
                            ),
                        ],
                    ),
                },
            ),
        )
        self.add_route(
            method="GET",
            path="/get-updates/{task_id}",
            controller_method=self.get_updates,
            doc=EndpointDocs(
                description="Get updates for the calculation tasks.",
                parameters={
                    "task_id": ParameterInfo(
                        description="Task ID to get updates.",
                        example="92a877b1-b657-4d0e-a749-9f4f244fdca2",
                    ),
                },
                responses={
                    200: ResponseInfo(
                        description="Object with the calculation result.",
                        content=[
                            ContentInfo(
                                type=CalculationResult[List[SportsGround]],
                                examples=[
                                    CalculationResult(
                                        type=ResultType.ID,
                                        status=ResultStatus.SUCCESS,
                                        data=[
                                            SportsGround(
                                                id=GroundId(406671453),
                                                object_name="object_name",
                                                location=Location(
                                                    adm_area="adm_area",
                                                    district="district",
                                                    address="address",
                                                    latitude=55.753215,
                                                    longitude=37.622504,
                                                ),
                                                contact=Contact(
                                                    email="email",
                                                    website="website",
                                                    phone="phone",
                                                ),
                                                conditions=Conditions(
                                                    has_equipment_rental=True,
                                                    has_tech_service=True,
                                                    has_dressing_room=True,
                                                    has_eatery=True,
                                                    has_toilet=True,
                                                    has_wifi=True,
                                                    has_cash_machine=True,
                                                    has_first_aid_post=True,
                                                    has_music=True,
                                                    lighting="смешанное",
                                                    seats=50,
                                                    paid="бесплатно",
                                                ),
                                            )
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    404: ResponseInfo(strings.GROUNDS_NOT_FOUND),
                },
            ),
        )
        self.add_route(
            method="POST",
            path="/search",
            controller_method=self.search_grounds,
            doc=EndpointDocs(
                description="Search sports grounds by the given criteria.",
                parameters={
                    "count": ParameterInfo(
                        description="Number of grounds to return.",
                        example="5",
                    ),
                },
                responses={
                    200: ResponseInfo(
                        description="Task ID to get updates.",
                        content=[
                            ContentInfo(
                                type=CalculationResult[TaskId],
                                examples=[
                                    CalculationResult(
                                        type=ResultType.ID,
                                        status=ResultStatus.SUCCESS,
                                        data=TaskId("92a877b1-b657-4d0e-a749-9f4f244fdca2"), # noqa
                                    ),
                                ],
                            ),
                        ],
                    ),
                },
            ),
        )
        self.add_route(
            method="POST",
            path="/like",
            controller_method=self.like_ground,
            doc=EndpointDocs(
                description="Like sports ground.",
                parameters={
                    "ground_id": ParameterInfo(
                        description="Ground ID to like.",
                        example="406671453",
                    ),
                },
                responses={
                    200: ResponseInfo("Ground liked by user {user.id}"),
                    404: ResponseInfo(strings.GROUNDS_NOT_FOUND),
                    400: ResponseInfo(strings.USER_ALREADY_LIKED_GROUND),
                },
            ),
        )
        self.add_route(
            method="GET",
            path="/recommendations",
            controller_method=self.get_recommendations,
            doc=EndpointDocs(
                description="Get recommendations for the user.",
                parameters={
                    "ground_id": ParameterInfo(
                        description="Ground ID to like.",
                        example="406671453",
                    ),
                    "count": ParameterInfo(
                        required=False,
                        description="Number of grounds to return.",
                        example="5",
                    ),
                },
                responses={
                    200: ResponseInfo(
                        description="Task ID to get updates.",
                        content=[
                            ContentInfo(
                                type=CalculationResult[TaskId],
                                examples=[
                                    CalculationResult(
                                        type=ResultType.ID,
                                        status=ResultStatus.SUCCESS,
                                        data=TaskId("92a877b1-b657-4d0e-a749-9f4f244fdca2"), # noqa
                                    ),
                                ],
                            ),
                        ],
                    ),
                },
            ),
        )
        self.add_route(
            method="DELETE",
            path="/like",
            controller_method=self.delete_like_ground,
            doc=EndpointDocs(
                description="Delete like for sports ground.",
                parameters={
                    "ground_id": ParameterInfo(
                        description="Ground ID to delete like.",
                        example="406671453",
                    ),
                },
                responses={
                    200: ResponseInfo(
                        "Ground unliked by user 35868fa8-e98a-48e8-9507-8c8422c957fd" # noqa
                    ),
                    404: ResponseInfo(strings.USER_DOES_NOT_LIKE_GROUND),
                },
            ),
        )
        self.add_route(
            method="GET",
            path="my",
            controller_method=self.get_user_grounds,
            doc=EndpointDocs(
                description="Get user-favorite sports grounds",
                responses={
                    200: ResponseInfo(
                        description="List of user's liked grounds.",
                        content=[
                            ContentInfo(
                                type=List[SportsGround],
                            ),
                        ],
                    ),
                },
            ),
        )
