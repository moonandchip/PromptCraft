from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.round.data.entities import Attempt

from .entities import Challenge


def get_user_archive(session: Session, user_id: str, limit: int = 30) -> list[dict]:
    """Returns the user's per-challenge results for the most recent `limit`
    challenges, newest first. Each entry is a dict with the challenge metadata
    plus the user's `attempts_used` and `best_score` (or 0 / 0.0 if they
    didn't play that day).
    """
    challenges_query = (
        select(Challenge)
        .order_by(Challenge.period_start.desc())
        .limit(limit)
    )
    challenges = list(session.execute(challenges_query).scalars())

    if not challenges:
        return []

    challenge_ids = [c.id for c in challenges]
    progress_query = (
        select(
            Attempt.challenge_id,
            func.count(Attempt.id).label("attempts_used"),
            func.coalesce(func.max(Attempt.similarity_score), 0).label("best_score"),
        )
        .where(Attempt.user_id == user_id, Attempt.challenge_id.in_(challenge_ids))
        .group_by(Attempt.challenge_id)
    )
    progress_by_id = {
        str(row.challenge_id): (int(row.attempts_used), float(row.best_score or 0.0))
        for row in session.execute(progress_query).all()
    }

    return [
        {
            "challenge_id": str(c.id),
            "period_start": c.period_start,
            "period_end": c.period_end,
            "round_id": c.round_id,
            "max_attempts": c.max_attempts,
            "attempts_used": progress_by_id.get(str(c.id), (0, 0.0))[0],
            "best_score": progress_by_id.get(str(c.id), (0, 0.0))[1],
        }
        for c in challenges
    ]
