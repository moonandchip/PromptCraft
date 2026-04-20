import logging

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse

from ..constants import CHANNEL, GET_LEADERBOARD_FEATURE, LEADERBOARD_LIMIT
from ..exceptions import ChallengeError, GetLeaderboardException
from ..models import LeaderboardResponse
from ..service import get_leaderboard_view
from ..types.args import GetLeaderboardArgs
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def leaderboard_endpoint(
    limit: int = Query(default=LEADERBOARD_LIMIT, ge=1, le=100),
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[LeaderboardResponse]:
    try:
        args = GetLeaderboardArgs(limit=limit)
        result = get_leaderboard_view(session=session, args=args)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in get_leaderboard",
            extra={"channel": CHANNEL, "feature": GET_LEADERBOARD_FEATURE, "error": str(exc), "user": current_user.id},
        )
        raise GetLeaderboardException(ChallengeError.UNKNOWN_ERROR) from exc
