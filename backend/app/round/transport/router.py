from fastapi import APIRouter, status

from ..constants import ROUTER_PREFIX, ROUTER_TAG
from ..models import AttemptInfo, RoundInfo, StartRoundResponse, SubmitRequest, SubmitResponse
from .get_round_attempts_endpoint import get_round_attempts_endpoint
from .get_rounds_endpoint import get_rounds_endpoint
from .start_endpoint import start_endpoint
from .submit_endpoint import submit_endpoint

router = APIRouter(prefix=ROUTER_PREFIX, tags=[ROUTER_TAG])

router.add_api_route(
    path="/rounds",
    endpoint=get_rounds_endpoint,
    methods=["GET"],
    response_model=list[RoundInfo],
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    path="/submit",
    endpoint=submit_endpoint,
    methods=["POST"],
    response_model=SubmitResponse,
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    path="/start",
    endpoint=start_endpoint,
    methods=["POST"],
    response_model=StartRoundResponse,
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    path="/{id}/attempts",
    endpoint=get_round_attempts_endpoint,
    methods=["GET"],
    response_model=list[AttemptInfo],
    status_code=status.HTTP_200_OK,
)
