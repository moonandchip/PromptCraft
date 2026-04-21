from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.round.data.entities import Attempt, UserProfile


def get_leaderboard(
    session: Session,
    challenge_id: str,
    limit: int,
) -> list[tuple[str, str, float, int]]:
    """Returns top scores for a challenge, one row per user.

    Args:
        session: SQLAlchemy session.
        challenge_id: Challenge UUID (string form) to scope the leaderboard.
        limit: Maximum number of entries to return.

    Returns:
        A list of (user_id, display_name, best_score, attempts_used) tuples,
        ordered by best_score descending.
    """
    best_score = func.max(Attempt.similarity_score).label("best_score")
    attempts_used = func.count(Attempt.id).label("attempts_used")

    query = (
        select(
            Attempt.user_id.label("user_id"),
            UserProfile.display_name.label("display_name"),
            UserProfile.email.label("email"),
            best_score,
            attempts_used,
        )
        .join(UserProfile, UserProfile.id == Attempt.user_id, isouter=True)
        .where(Attempt.challenge_id == challenge_id)
        .group_by(Attempt.user_id, UserProfile.display_name, UserProfile.email)
        .order_by(best_score.desc())
        .limit(limit)
    )
    rows = session.execute(query).all()
    results: list[tuple[str, str, float, int]] = []
    for row in rows:
        display = row.display_name or (row.email.split("@")[0] if row.email else "anonymous")
        results.append((str(row.user_id), str(display), float(row.best_score or 0.0), int(row.attempts_used or 0)))
    return results
