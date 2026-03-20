from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse

from ..models import AttemptInfo
from ..service import get_round_attempts
from .get_db_session import get_db_session


def get_round_attempts_endpoint(
    id: str,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> list[AttemptInfo]:
    """Handles returning all attempts for the authenticated user and round.

    Args:
        id: The round ID path parameter.
        current_user: The authenticated user requesting attempts.
        session: The SQLAlchemy session used for persistence operations.

    Returns:
        A list of round attempts ordered by attempt number.

    Raises:
        Exception: Propagates service-layer errors.
    """
    return get_round_attempts(session=session, user_id=current_user.id, round_id=id)
