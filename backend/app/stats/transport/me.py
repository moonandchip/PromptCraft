from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse

from ..models import StatsResponse
from ..service import get_user_stats
from .get_db_session import get_db_session


def me_stats_endpoint(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> StatsResponse:
    """Handles returning gameplay stats for the authenticated user.

    Args:
        current_user: The authenticated user requesting gameplay stats.
        session: The SQLAlchemy session used to retrieve stats data.

    Returns:
        A stats response for the authenticated user.

    Raises:
        Exception: Propagates authentication or service-layer errors.
    """
    return get_user_stats(session=session, user_id=current_user.id)
