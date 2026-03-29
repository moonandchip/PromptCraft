import logging

from ..constants import CHANNEL, REGISTER_FEATURE
from ..exceptions import AuthError, RegisterException

from ..constants import ERR_INVALID_AUTH_REGISTER_RESPONSE
from ..data.post_register import post_register
from ..models import RegisterRequest, UserResponse
from .errors import AuthServiceError
from .extract_user_from_response import extract_user_from_response
from .types import AuthServiceConfig

logger = logging.getLogger(__name__)


def register_user(payload: RegisterRequest, config: AuthServiceConfig) -> UserResponse:
    try:
        response = post_register(
            email=payload.email,
            password=payload.password,
            name=payload.name,
            base_url=config.base_url,
            timeout_seconds=config.timeout_seconds,
        )
    except AuthServiceError as exc:
        raise RegisterException(
            AuthError.INVALID_CREDENTIALS, message=exc.detail,
        ) from exc

    try:
        user = extract_user_from_response(response, ERR_INVALID_AUTH_REGISTER_RESPONSE)
    except AuthServiceError as exc:
        raise RegisterException(
            AuthError.SERVICE_UNAVAILABLE, message=exc.detail,
        ) from exc

    logger.info(
        "User registered",
        extra={"channel": CHANNEL, "feature": REGISTER_FEATURE, "user": payload.email},
    )

    return user
