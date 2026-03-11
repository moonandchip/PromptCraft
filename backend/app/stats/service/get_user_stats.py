from sqlalchemy.orm import Session

from app.stats.data import get_rounds_aggregates_by_user_id
from app.stats.models import StatsResponse


def get_user_stats(session: Session, user_id: str) -> StatsResponse:
    """Builds the stats response for a specific user.

    Args:
        session: The SQLAlchemy session used to access round aggregate data.
        user_id: The ID of the user whose stats are being requested.

    Returns:
        A stats response model with rounds played, average score, and best score.

    Raises:
        Exception: Propagates errors raised by the data access layer.
    """
    rounds_played, average_score, best_score = get_rounds_aggregates_by_user_id(session=session, user_id=user_id)
    return StatsResponse(
        rounds_played=rounds_played,
        average_score=average_score,
        best_score=best_score,
    )
