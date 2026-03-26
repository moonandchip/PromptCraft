import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse
from ..constants import CHANNEL, GET_ROUND_HISTORY_FEATURE
from app.round.exceptions import RoundError, GetRoundHistoryException

from ..models import RoundHistoryResponse
from ..service import get_round_history
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def get_round_history_endpoint(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[list[RoundHistoryResponse]]:
    try:
        result = get_round_history(session=session, user_id=current_user.id)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in get_round_history",
            extra={"channel": CHANNEL, "feature": GET_ROUND_HISTORY_FEATURE, "error": str(exc), "user": current_user.id},
        )
        raise GetRoundHistoryException(RoundError.UNKNOWN_ERROR) from exc
