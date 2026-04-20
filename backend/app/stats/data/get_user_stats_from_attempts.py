from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.round.data.entities import Attempt, Prompt
from app.stats.data.entities import Round


def get_user_stats_from_attempts(
    session: Session,
    user_id: str,
    recent_limit: int = 5,
) -> dict:
    """Retrieves comprehensive user stats derived from the attempts table.

    `total_rounds` counts play sessions: one per row in `rounds` (each
    practice round start) plus one per distinct `challenge_id` the user
    has played. Counting distinct `Attempt.round_id` would cap at the
    number of unique round slugs, not sessions.
    """
    agg_query = (
        select(
            func.count(Attempt.id).label("total_attempts"),
            func.coalesce(func.avg(Attempt.similarity_score), 0).label("average_score"),
            func.coalesce(func.max(Attempt.similarity_score), 0).label("best_score"),
        )
        .where(Attempt.user_id == user_id)
    )
    row = session.execute(agg_query).one()

    practice_rounds = session.execute(
        select(func.count(Round.id)).where(Round.user_id == user_id)
    ).scalar() or 0

    challenge_rounds = session.execute(
        select(func.count(func.distinct(Attempt.challenge_id)))
        .where(Attempt.user_id == user_id, Attempt.challenge_id.isnot(None))
    ).scalar() or 0

    recent_query = (
        select(
            Attempt.round_id,
            Attempt.attempt_number,
            Prompt.prompt_text.label("prompt"),
            Attempt.generated_image_url,
            Attempt.similarity_score,
            Attempt.created_at,
        )
        .join(Prompt, Prompt.id == Attempt.prompt_id)
        .where(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc())
        .limit(recent_limit)
    )
    recent_rows = session.execute(recent_query).all()

    return {
        "total_rounds": int(practice_rounds) + int(challenge_rounds),
        "total_attempts": int(row.total_attempts or 0),
        "average_score": round(float(row.average_score or 0.0), 1),
        "best_score": float(row.best_score or 0.0),
        "recent_attempts": [
            {
                "round_id": str(r.round_id),
                "attempt_number": int(r.attempt_number),
                "prompt": str(r.prompt),
                "generated_image_url": str(r.generated_image_url),
                "similarity_score": float(r.similarity_score or 0.0),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in recent_rows
        ],
    }
