from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .entities import Attempt


def get_next_attempt_number(session: Session, user_id: str, round_id: str) -> int:
    """Calculates the next attempt number for a user/round pair.

    Args:
        session: The SQLAlchemy session used for data access.
        user_id: The ID of the user attempting the round.
        round_id: The round ID for the attempt.

    Returns:
        The next 1-based attempt number for this user/round pair.

    Raises:
        Exception: Propagates database errors raised by the session.
    """
    max_attempt_number = session.execute(
        select(func.max(Attempt.attempt_number)).where(
            Attempt.user_id == user_id,
            Attempt.round_id == round_id,
        )
    ).scalar_one()
    return int(max_attempt_number or 0) + 1
