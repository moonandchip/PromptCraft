from fastapi import Depends

from ..models import UserResponse
from .get_current_user import get_current_user


def me_endpoint(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Transport handler that returns the already-resolved current user."""
    return current_user
