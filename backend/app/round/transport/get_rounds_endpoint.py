from app.response import ApiResponse

from ..models import RoundInfo
from ..service import get_rounds


def get_rounds_endpoint() -> ApiResponse[list[RoundInfo]]:
    return ApiResponse(data=get_rounds())
