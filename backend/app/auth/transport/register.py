import logging

from fastapi import Depends

from app.exceptions import AppException
from app.response import ApiResponse

from ..constants import CHANNEL, REGISTER_FEATURE
from ..exceptions import AuthError, RegisterException

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
        logger.error(
            "Unexpected error in register",
            extra={"channel": CHANNEL, "feature": REGISTER_FEATURE, "error": str(exc), "user": payload.email},
        )
        raise RegisterException(AuthError.UNKNOWN_ERROR) from exc
