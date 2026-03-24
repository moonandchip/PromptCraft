import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse
from app.constants import ROUND_CHANNEL
from app.round.constants import GET_ROUND_ATTEMPTS_FEATURE
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
        logger.exception(
            "Unexpected error in get_round_attempts",
            extra={"channel": ROUND_CHANNEL, "feature": GET_ROUND_ATTEMPTS_FEATURE, "user": current_user.id},
        )
        raise GetRoundAttemptsException(
            status_code=500, error_code=RoundError.UNKNOWN_ERROR, message="An unexpected error occurred",
        ) from exc
