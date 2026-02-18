from fastapi import APIRouter, status

from ..constants import ROUTER_PREFIX, ROUTER_TAG
from ..models import TokenResponse, UserResponse
from .login import login_endpoint
from .me import me_endpoint
from .register import register

router = APIRouter(prefix=ROUTER_PREFIX, tags=[ROUTER_TAG])

router.add_api_route(
    path="/register",
    endpoint=register,
    methods=["POST"],
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    path="/login",
    endpoint=login_endpoint,
    methods=["POST"],
    response_model=TokenResponse,
)

router.add_api_route(
    path="/me",
    endpoint=me_endpoint,
    methods=["GET"],
    response_model=UserResponse,
)
