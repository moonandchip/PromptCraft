from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .entities import Challenge


def get_active_challenge(session: Session, period_type: str, now: datetime) -> Challenge | None:
    """Returns the active challenge of the given period type, if any.

    Args:
        session: SQLAlchemy session.
        period_type: Period bucket to scope the lookup ("daily", "weekly").
        now: Reference timestamp the challenge must straddle.

    Returns:
        The matching Challenge row, or None if no active challenge exists.
    """
    query = (
        select(Challenge)
        .where(
            Challenge.period_type == period_type,
            Challenge.period_start <= now,
            Challenge.period_end > now,
        )
        .order_by(Challenge.period_start.desc())
        .limit(1)
    )
    return session.execute(query).scalar_one_or_none()
