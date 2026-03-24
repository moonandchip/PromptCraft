from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.exceptions import AuthError, ResolveTokenException

from ..constants import BEARER_SCHEME, ERR_MISSING_BEARER_TOKEN
from ..models import UserResponse
from ..service.resolve_user_from_token import resolve_user_from_token
from ..service.types import AuthServiceConfig
from .get_auth_service import get_auth_service

_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    auth_service: AuthServiceConfig = Depends(get_auth_service),
) -> UserResponse:
    if credentials is None or credentials.scheme.lower() != BEARER_SCHEME:
        raise ResolveTokenException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=AuthError.INVALID_TOKEN,
            message=ERR_MISSING_BEARER_TOKEN,
        )

    return resolve_user_from_token(token=credentials.credentials, config=auth_service)
