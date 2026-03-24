from fastapi import APIRouter, status

from ..constants import ROUTER_PREFIX, ROUTER_TAG
from ..models import TokenResponse, UserResponse
from app.response import ApiResponse
from .login import login_endpoint
from .me import me_endpoint
from .register import register_endpoint

router = APIRouter(prefix=ROUTER_PREFIX, tags=[ROUTER_TAG])

router.add_api_route(
    path="/register",
    endpoint=register_endpoint,
    methods=["POST"],
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    path="/login",
    endpoint=login_endpoint,
    methods=["POST"],
    response_model=ApiResponse[TokenResponse],
)

router.add_api_route(
    path="/me",
    endpoint=me_endpoint,
    methods=["GET"],
    response_model=ApiResponse[UserResponse],
)
