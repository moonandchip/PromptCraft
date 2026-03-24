from app.auth.domain.exceptions import AuthError, ResolveTokenException

from ..constants import ERR_INVALID_AUTH_ME_RESPONSE
from ..data.get_internal_me import get_internal_me
from ..models import UserResponse
from .errors import AuthServiceError
from .extract_user_from_response import extract_user_from_response
from .types import AuthServiceConfig


def resolve_user_from_token(token: str, config: AuthServiceConfig) -> UserResponse:
    try:
        response = get_internal_me(
            token=token,
            base_url=config.base_url,
            timeout_seconds=config.timeout_seconds,
        )
    except AuthServiceError as exc:
        raise ResolveTokenException(
            status_code=exc.status_code, error_code=AuthError.INVALID_TOKEN, message=exc.detail,
        ) from exc

    try:
        return extract_user_from_response(response, ERR_INVALID_AUTH_ME_RESPONSE)
    except AuthServiceError as exc:
        raise ResolveTokenException(
            status_code=exc.status_code, error_code=AuthError.SERVICE_UNAVAILABLE, message=exc.detail,
        ) from exc
