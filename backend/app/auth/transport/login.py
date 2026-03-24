import logging

from fastapi import Depends

from app.exceptions import AppException
from app.response import ApiResponse
from app.constants import AUTH_CHANNEL
from app.auth.domain.constants import LOGIN_FEATURE
from app.auth.domain.exceptions import AuthError, LoginException

from ..models import LoginRequest, TokenResponse
from ..service.login import login
from ..service.types import AuthServiceConfig
from .get_auth_service import get_auth_service

logger = logging.getLogger(__name__)


def login_endpoint(
    payload: LoginRequest,
    auth_service: AuthServiceConfig = Depends(get_auth_service),
) -> ApiResponse[TokenResponse]:
    try:
        result = login(payload=payload, config=auth_service)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.exception(
            "Unexpected error in login",
            extra={"channel": AUTH_CHANNEL, "feature": LOGIN_FEATURE, "user": payload.email},
        )
        raise LoginException(
            status_code=500, error_code=AuthError.UNKNOWN_ERROR, message="An unexpected error occurred",
        ) from exc
