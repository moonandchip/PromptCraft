from ..constants import (
    ERR_INVALID_USER_PAYLOAD_FROM_AUTH_SERVICE,
    KEY_EMAIL,
    KEY_ID,
    KEY_NAME,
    KEY_USER,
)
from ..models import UserResponse
from .errors import AuthServiceError


def extract_user_from_response(response: dict, invalid_response_message: str) -> UserResponse:
    """Validate and normalize a user payload returned by the auth service."""
    user = response.get(KEY_USER)
    if not isinstance(user, dict):
        raise AuthServiceError(502, invalid_response_message)

    user_id = user.get(KEY_ID)
    email = user.get(KEY_EMAIL)
    if not isinstance(user_id, str) or not isinstance(email, str):
        raise AuthServiceError(502, ERR_INVALID_USER_PAYLOAD_FROM_AUTH_SERVICE)

    return UserResponse(
        id=user_id,
        email=email,
        name=user.get(KEY_NAME),
    )
