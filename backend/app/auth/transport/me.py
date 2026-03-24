from fastapi import Depends

from app.response import ApiResponse

from ..models import UserResponse
from .get_current_user import get_current_user


def me_endpoint(current_user: UserResponse = Depends(get_current_user)) -> ApiResponse[UserResponse]:
    return ApiResponse(data=current_user)
