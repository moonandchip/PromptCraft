from fastapi import Depends, HTTPException

from ..models import RegisterRequest, UserResponse
from ..service.errors import AuthServiceError
from ..service.register_user import register_user
from ..service.types import AuthServiceConfig
from .get_auth_service import get_auth_service


def register(
    payload: RegisterRequest,
    auth_service: AuthServiceConfig = Depends(get_auth_service),
) -> UserResponse:
    """Transport handler for user registration."""
    try:
        return register_user(payload=payload, config=auth_service)
    except AuthServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
