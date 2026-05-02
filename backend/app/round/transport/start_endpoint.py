import logging

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user_optional
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
    difficulty: str | None = Query(default=None, pattern="^(easy|medium|hard)$"),
    current_user: UserResponse | None = Depends(get_current_user_optional),
    session: Session = Depends(get_db_session),
) -> ApiResponse[RoundStartResponse]:
    try:
        args = StartRoundArgs(
            user_id=current_user.id if current_user else None,
            user_email=current_user.email if current_user else None,
            user_display_name=current_user.name if current_user else None,
            difficulty=difficulty,
        )
        result = start_round(session=session, args=args)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in start_round",
            extra={
                "channel": CHANNEL,
                "feature": START_ROUND_FEATURE,
                "error": str(exc),
                "user": current_user.id if current_user else "guest",
            },
        )
        raise StartRoundException(RoundError.UNKNOWN_ERROR) from exc
