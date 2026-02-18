from ..constants import ERR_INVALID_AUTH_ME_RESPONSE
from ..data.get_internal_me import get_internal_me
from ..models import UserResponse
from .extract_user_from_response import extract_user_from_response
from .types import AuthServiceConfig


def resolve_user_from_token(token: str, config: AuthServiceConfig) -> UserResponse:
    """Resolve the authenticated user represented by a bearer token."""
    response = get_internal_me(
        token=token,
        base_url=config.base_url,
        timeout_seconds=config.timeout_seconds,
    )
    return extract_user_from_response(response, ERR_INVALID_AUTH_ME_RESPONSE)
