import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse
from ..constants import CHANNEL, GET_ROUND_ATTEMPTS_FEATURE
from app.round.exceptions import GetRoundAttemptsException, RoundError

from ..models import RoundAttemptResponse
from ..service import get_round_attempts
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def get_round_attempts_endpoint(
    id: str,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[list[RoundAttemptResponse]]:
    try:
        result = get_round_attempts(session=session, user_id=current_user.id, round_id=id)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in get_round_attempts",
            extra={"channel": CHANNEL, "feature": GET_ROUND_ATTEMPTS_FEATURE, "error": str(exc), "user": current_user.id},
        )
        raise GetRoundAttemptsException(RoundError.UNKNOWN_ERROR) from exc
