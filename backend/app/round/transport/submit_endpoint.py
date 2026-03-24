import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse
from app.constants import ROUND_CHANNEL
from app.round.constants import SUBMIT_ROUND_FEATURE
from app.round.exceptions import RoundError, SubmitRoundException

from ..models import RoundSubmitRequest, RoundSubmitResponse
from ..service import submit_round
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def submit_endpoint(
    body: RoundSubmitRequest,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[RoundSubmitResponse]:
    try:
        result = submit_round(
            session=session,
            user_email=current_user.email,
            round_id=body.round_id,
            user_prompt=body.user_prompt,
        )
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.exception(
            "Unexpected error in submit_round",
            extra={"channel": ROUND_CHANNEL, "feature": SUBMIT_ROUND_FEATURE, "user": current_user.email},
        )
        raise SubmitRoundException(
            status_code=500, error_code=RoundError.UNKNOWN_ERROR, message="An unexpected error occurred",
        ) from exc
