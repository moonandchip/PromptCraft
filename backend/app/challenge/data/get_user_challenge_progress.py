from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.round.data.entities import Attempt


def get_user_challenge_progress(
    session: Session,
    user_id: str,
    challenge_id: str,
) -> tuple[int, float]:
    """Returns (attempts_used, best_score) for a user against a single challenge.

    Args:
        session: SQLAlchemy session.
        user_id: Authenticated user ID.
        challenge_id: Challenge UUID (string form) to scope the aggregate.

    Returns:
        A two-tuple of (attempts_used, best_score). best_score is 0.0 when no attempts exist.
    """
    query = (
        select(
            func.count(Attempt.id).label("attempts_used"),
            func.coalesce(func.max(Attempt.similarity_score), 0).label("best_score"),
        )
        .where(
            Attempt.user_id == user_id,
            Attempt.challenge_id == challenge_id,
        )
    )
    row = session.execute(query).one()
    return int(row.attempts_used or 0), float(row.best_score or 0.0)
