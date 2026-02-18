from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..constants import BEARER_SCHEME, ERR_MISSING_BEARER_TOKEN
from ..models import UserResponse
from ..service.errors import AuthServiceError
from ..service.resolve_user_from_token import resolve_user_from_token
from ..service.types import AuthServiceConfig
from .get_auth_service import get_auth_service

_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    auth_service: AuthServiceConfig = Depends(get_auth_service),
) -> UserResponse:
    """Resolve authenticated user from bearer credentials for protected routes."""
    if credentials is None or credentials.scheme.lower() != BEARER_SCHEME:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ERR_MISSING_BEARER_TOKEN)

    try:
        return resolve_user_from_token(token=credentials.credentials, config=auth_service)
    except AuthServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
