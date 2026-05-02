from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..constants import BEARER_SCHEME
from ..models import UserResponse
from ..service.resolve_user_from_token import resolve_user_from_token
from ..service.types import AuthServiceConfig
from .get_auth_service import get_auth_service

_bearer = HTTPBearer(auto_error=False)


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    auth_service: AuthServiceConfig = Depends(get_auth_service),
) -> UserResponse | None:
    """Like get_current_user, but returns None instead of raising when the
    request is unauthenticated. Used for endpoints that allow guest access."""
    if credentials is None or credentials.scheme.lower() != BEARER_SCHEME:
        return None
    try:
        return resolve_user_from_token(token=credentials.credentials, config=auth_service)
    except Exception:
        return None
