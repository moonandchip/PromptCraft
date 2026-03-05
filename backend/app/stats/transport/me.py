from fastapi import Depends

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse

from ..db import get_db_connection
from ..models import StatsResponse
from ..service import get_user_stats


def me_stats_endpoint(
    current_user: UserResponse = Depends(get_current_user),
    connection: object = Depends(get_db_connection),
) -> StatsResponse:
    return get_user_stats(connection=connection, user_id=current_user.id)
