import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse

from ..constants import CHANNEL, SUBMIT_CHALLENGE_FEATURE
from ..exceptions import ChallengeError, SubmitChallengeException
from ..models import ChallengeSubmitRequest, ChallengeSubmitResponse
from ..service import submit_challenge
from ..types.args import SubmitChallengeArgs
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def submit_endpoint(
    body: ChallengeSubmitRequest,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[ChallengeSubmitResponse]:
    try:
        args = SubmitChallengeArgs(
            user_id=current_user.id,
            user_email=current_user.email,
            user_prompt=body.user_prompt,
            user_display_name=current_user.name,
        )
        result = submit_challenge(session=session, args=args)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in submit_challenge",
            extra={"channel": CHANNEL, "feature": SUBMIT_CHALLENGE_FEATURE, "error": str(exc), "user": current_user.email},
        )
        raise SubmitChallengeException(ChallengeError.UNKNOWN_ERROR) from exc
