import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse
from ..constants import CHANNEL, SUBMIT_ROUND_FEATURE
from app.round.exceptions import RoundError, SubmitRoundException

from ..models import RoundSubmitRequest, RoundSubmitResponse
from ..service import submit_round
from ..types.args import SubmitRoundArgs
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def submit_endpoint(
    body: RoundSubmitRequest,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[RoundSubmitResponse]:
    try:
        args = SubmitRoundArgs(user_email=current_user.email, round_id=body.round_id, user_prompt=body.user_prompt)
        result = submit_round(session=session, args=args)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in submit_round",
            extra={"channel": CHANNEL, "feature": SUBMIT_ROUND_FEATURE, "error": str(exc), "user": current_user.email},
        )
        raise SubmitRoundException(RoundError.UNKNOWN_ERROR) from exc
