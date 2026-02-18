from fastapi import Depends, HTTPException

from ..models import LoginRequest, TokenResponse
from ..service.errors import AuthServiceError
from ..service.login import login
from ..service.types import AuthServiceConfig
from .get_auth_service import get_auth_service


def login_endpoint(
    payload: LoginRequest,
    auth_service: AuthServiceConfig = Depends(get_auth_service),
) -> TokenResponse:
    """Transport handler for credentials login."""
    try:
        return login(payload=payload, config=auth_service)
    except AuthServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
