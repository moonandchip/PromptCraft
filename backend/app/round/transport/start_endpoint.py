import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse
from app.constants import ROUND_CHANNEL
from app.round.domain.constants import START_ROUND_FEATURE
from app.round.domain.exceptions import RoundError, StartRoundException

from ..models import RoundStartResponse
from ..service import start_round
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def start_endpoint(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[RoundStartResponse]:
    try:
        result = start_round(session=session, user_id=current_user.id)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.exception(
            "Unexpected error in start_round",
            extra={"channel": ROUND_CHANNEL, "feature": START_ROUND_FEATURE, "user": current_user.id},
        )
        raise StartRoundException(
            status_code=500, error_code=RoundError.UNKNOWN_ERROR, message="An unexpected error occurred",
        ) from exc
