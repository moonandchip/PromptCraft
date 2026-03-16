from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse

from ..models import StartRoundResponse
from ..service import RoundServiceError, start_round
from .get_db_session import get_db_session


def start_endpoint(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> StartRoundResponse:
    """Handles starting a new round for the authenticated user.

    Args:
        current_user: The authenticated user starting a practice round.
        session: The SQLAlchemy session used for persistence operations.

    Returns:
        A start-round response with round ID and target image URL.

    Raises:
        HTTPException: If the service layer fails to start or persist the round.
    """
    try:
        return start_round(session=session, user_id=current_user.id)
    except RoundServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
