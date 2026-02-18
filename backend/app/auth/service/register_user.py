from ..constants import ERR_INVALID_AUTH_REGISTER_RESPONSE
from ..data.post_register import post_register
from ..models import RegisterRequest, UserResponse
from .extract_user_from_response import extract_user_from_response
from .types import AuthServiceConfig


def register_user(payload: RegisterRequest, config: AuthServiceConfig) -> UserResponse:
    """Register a user via auth service and return normalized user output."""
    response = post_register(
        email=payload.email,
        password=payload.password,
        name=payload.name,
        base_url=config.base_url,
        timeout_seconds=config.timeout_seconds,
    )
    return extract_user_from_response(response, ERR_INVALID_AUTH_REGISTER_RESPONSE)
