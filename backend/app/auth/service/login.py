from ..constants import BEARER_SCHEME, ERR_INVALID_AUTH_TOKEN_RESPONSE, KEY_ACCESS_TOKEN, KEY_TOKEN_TYPE
from ..data.post_internal_login import post_internal_login
from ..models import LoginRequest, TokenResponse
from .errors import AuthServiceError
from .types import AuthServiceConfig


def login(payload: LoginRequest, config: AuthServiceConfig) -> TokenResponse:
    """Authenticate credentials via auth service and return a token response."""
    response = post_internal_login(
        email=payload.email,
        password=payload.password,
        base_url=config.base_url,
        timeout_seconds=config.timeout_seconds,
    )

    token = response.get(KEY_ACCESS_TOKEN)
    token_type = response.get(KEY_TOKEN_TYPE, BEARER_SCHEME)
    if not isinstance(token, str):
        raise AuthServiceError(502, ERR_INVALID_AUTH_TOKEN_RESPONSE)

    return TokenResponse(access_token=token, token_type=str(token_type))
