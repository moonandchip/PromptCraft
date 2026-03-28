import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse
from ..constants import CHANNEL, START_ROUND_FEATURE
from app.round.exceptions import RoundError, StartRoundException

from ..models import RoundStartResponse
from ..service import start_round
from ..types.args import StartRoundArgs
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def start_endpoint(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[RoundStartResponse]:
    try:
        args = StartRoundArgs(user_id=current_user.id, user_email=current_user.email, user_display_name=current_user.name)
        result = start_round(session=session, args=args)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in start_round",
            extra={"channel": CHANNEL, "feature": START_ROUND_FEATURE, "error": str(exc), "user": current_user.id},
        )
        raise StartRoundException(RoundError.UNKNOWN_ERROR) from exc
