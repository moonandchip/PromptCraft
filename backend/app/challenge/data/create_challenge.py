from datetime import datetime

from sqlalchemy.orm import Session

from .entities import Challenge


def create_challenge(
    session: Session,
    period_type: str,
    period_start: datetime,
    period_end: datetime,
    round_id: str,
    max_attempts: int,
) -> Challenge:
    """Persists a new challenge row and returns the managed entity."""
    row = Challenge(
        period_type=period_type,
        period_start=period_start,
        period_end=period_end,
        round_id=round_id,
        max_attempts=max_attempts,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row
