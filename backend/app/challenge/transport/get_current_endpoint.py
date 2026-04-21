import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse

from ..constants import CHANNEL, GET_CURRENT_FEATURE
from ..exceptions import ChallengeError, GetCurrentChallengeException
from ..models import ChallengeStateResponse
from ..service import get_current_challenge_view
from ..types.args import GetCurrentChallengeArgs
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def get_current_endpoint(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[ChallengeStateResponse]:
    try:
        args = GetCurrentChallengeArgs(user_id=current_user.id)
        result = get_current_challenge_view(session=session, args=args)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in get_current_challenge",
            extra={"channel": CHANNEL, "feature": GET_CURRENT_FEATURE, "error": str(exc), "user": current_user.id},
        )
        raise GetCurrentChallengeException(ChallengeError.UNKNOWN_ERROR) from exc
