import logging

from fastapi import Depends

from app.exceptions import AppException
from app.response import ApiResponse

from ..constants import CHANNEL, LOGIN_FEATURE
from ..exceptions import AuthError, LoginException

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
        logger.error(
            "Unexpected error in login",
            extra={"channel": CHANNEL, "feature": LOGIN_FEATURE, "error": str(exc), "user": payload.email},
        )
        raise LoginException(AuthError.UNKNOWN_ERROR) from exc
