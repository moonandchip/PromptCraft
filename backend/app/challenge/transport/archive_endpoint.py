import logging

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.exceptions import AppException
from app.response import ApiResponse

from ..constants import ARCHIVE_DEFAULT_LIMIT, ARCHIVE_MAX_LIMIT, CHANNEL, GET_ARCHIVE_FEATURE
from ..exceptions import ChallengeError, GetArchiveException
from ..models import ArchiveResponse
from ..service import get_archive_view
from ..types.args import GetArchiveArgs
from .get_db_session import get_db_session

logger = logging.getLogger(__name__)


def archive_endpoint(
    limit: int = Query(default=ARCHIVE_DEFAULT_LIMIT, ge=1, le=ARCHIVE_MAX_LIMIT),
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ApiResponse[ArchiveResponse]:
    try:
        args = GetArchiveArgs(user_id=current_user.id, limit=limit)
        result = get_archive_view(session=session, args=args)
        return ApiResponse(data=result)
    except AppException:
        raise
    except Exception as exc:
        logger.error(
            "Unexpected error in get_archive",
            extra={"channel": CHANNEL, "feature": GET_ARCHIVE_FEATURE, "error": str(exc), "user": current_user.id},
        )
        raise GetArchiveException(ChallengeError.UNKNOWN_ERROR) from exc
