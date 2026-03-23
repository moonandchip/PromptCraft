from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .entities import Round


def get_rounds_aggregates_by_user_id(session: Session, user_id: str) -> tuple[int, float, float]:
    """Retrieves round aggregate metrics for a specific user.

    Args:
        session: The SQLAlchemy session used to execute the aggregate query.
        user_id: The ID of the user whose round statistics are being retrieved.

    Returns:
        A tuple containing rounds played, average score, and best score.

    Raises:
        Exception: Propagates database execution errors raised by the session.
    """
    query = (
        select(
            func.count(Round.id).label("rounds_played"),
            func.coalesce(func.avg(Round.score), 0).label("average_score"),
            func.coalesce(func.max(Round.score), 0).label("best_score"),
        )
        .select_from(Round)
        .where(Round.user_id == user_id)
    )
    row = session.execute(query).one()
    return int(row.rounds_played or 0), float(row.average_score or 0.0), float(row.best_score or 0.0)

from .entities import Round
from .get_rounds_aggregates_by_user_id import get_rounds_aggregates_by_user_id

__all__ = ["Round", "get_rounds_aggregates_by_user_id"]