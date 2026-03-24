import logging

from fastapi import Depends

from app.exceptions import AppException
from app.response import ApiResponse
from app.constants import AUTH_CHANNEL
from app.auth.constants import REGISTER_FEATURE
from app.auth.exceptions import AuthError, RegisterException

from ..models import RegisterRequest, UserResponse
from ..service.register_user import register_user
from ..service.types import AuthServiceConfig
from .get_auth_service import get_auth_service

logger = logging.getLogger(__name__)


def register_endpoint(
    payload: RegisterRequest,
    auth_service: AuthServiceConfig = Depends(get_auth_service),
) -> ApiResponse[UserResponse]:
    try:
        result = register_user(payload=payload, config=auth_service)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.exception(
            "Unexpected error in register",
            extra={"channel": AUTH_CHANNEL, "feature": REGISTER_FEATURE, "user": payload.email},
        )
        raise RegisterException(
            status_code=500, error_code=AuthError.UNKNOWN_ERROR, message="An unexpected error occurred",
        ) from exc
