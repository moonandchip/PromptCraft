from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .entities import Attempt


def get_round_history_by_user_id(
    session: Session,
    user_id: str,
) -> list[tuple[str, float, int]]:
    """Retrieves distinct rounds played by a user with their best score.

    Args:
        session: The SQLAlchemy session used for data access.
        user_id: The authenticated user ID.

    Returns:
        A list of tuples: (round_id, best_score, attempt_count).
    """
    query = (
        select(
            Attempt.round_id.label("round_id"),
            func.max(Attempt.similarity_score).label("best_score"),
            func.count(Attempt.id).label("attempt_count"),
        )
        .where(Attempt.user_id == user_id)
        .group_by(Attempt.round_id)
        .order_by(func.max(Attempt.created_at).desc())
    )
    rows = session.execute(query).all()
    return [
        (str(row.round_id), float(row.best_score or 0.0), int(row.attempt_count))
        for row in rows
    ]
