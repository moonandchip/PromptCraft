import logging

from app.constants import AUTH_CHANNEL
from app.auth.constants import LOGIN_FEATURE
from app.auth.exceptions import AuthError, LoginException

from ..constants import BEARER_SCHEME, KEY_ACCESS_TOKEN, KEY_TOKEN_TYPE
from ..data.post_internal_login import post_internal_login
from ..models import LoginRequest, TokenResponse
from .errors import AuthServiceError
from .types import AuthServiceConfig

logger = logging.getLogger(__name__)


def login(payload: LoginRequest, config: AuthServiceConfig) -> TokenResponse:
    try:
        response = post_internal_login(
            email=payload.email,
            password=payload.password,
            base_url=config.base_url,
            timeout_seconds=config.timeout_seconds,
        )
    except AuthServiceError as exc:
        raise LoginException(
            status_code=exc.status_code, error_code=AuthError.INVALID_CREDENTIALS, message=exc.detail,
        ) from exc

    token = response.get(KEY_ACCESS_TOKEN)
    token_type = response.get(KEY_TOKEN_TYPE, BEARER_SCHEME)
    if not isinstance(token, str):
        raise LoginException(
            status_code=502, error_code=AuthError.SERVICE_UNAVAILABLE, message="Invalid auth token response",
        )

    logger.info(
        "User logged in",
        extra={"channel": AUTH_CHANNEL, "feature": LOGIN_FEATURE, "user": payload.email},
    )

    return TokenResponse(access_token=token, token_type=str(token_type))
