from fastapi import APIRouter, status

from app.response import ApiResponse

from ..constants import ROUTER_PREFIX, ROUTER_TAG
from ..models import ChallengeStateResponse, ChallengeSubmitResponse, LeaderboardResponse
from .get_current_endpoint import get_current_endpoint
from .leaderboard_endpoint import leaderboard_endpoint
from .submit_endpoint import submit_endpoint

router = APIRouter(prefix=ROUTER_PREFIX, tags=[ROUTER_TAG])

router.add_api_route(
    path="/current",
    endpoint=get_current_endpoint,
    methods=["GET"],
    response_model=ApiResponse[ChallengeStateResponse],
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    path="/submit",
    endpoint=submit_endpoint,
    methods=["POST"],
    response_model=ApiResponse[ChallengeSubmitResponse],
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    path="/leaderboard",
    endpoint=leaderboard_endpoint,
    methods=["GET"],
    response_model=ApiResponse[LeaderboardResponse],
    status_code=status.HTTP_200_OK,
)
