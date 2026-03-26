import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse

from ..constants import CHANNEL, GET_STATS_FEATURE
from ..exceptions import GetStatsException, StatsError

from ..models import StatsResponse
from ..service import get_user_stats
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def me_stats_endpoint(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[StatsResponse]:
    try:
        result = get_user_stats(session=session, user_id=current_user.id)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in get_user_stats",
            extra={"channel": CHANNEL, "feature": GET_STATS_FEATURE, "error": str(exc), "user": current_user.id},
        )
        raise GetStatsException(StatsError.UNKNOWN_ERROR) from exc
