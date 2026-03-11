from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .entities import Attempt


def get_next_attempt_number(session: Session, user_id: str, image_id: str) -> int:
    """Calculates the next attempt number for a user/image pair.

    Args:
        session: The SQLAlchemy session used for data access.
        user_id: The ID of the user attempting the round.
        image_id: The ID of the reference image for the round.

    Returns:
        The next 1-based attempt number for this user/image pair.

    Raises:
        Exception: Propagates database errors raised by the session.
    """
    existing_attempts = session.execute(
        select(func.count(Attempt.id)).where(Attempt.user_id == user_id, Attempt.image_id == image_id)
    ).scalar_one()
    return int(existing_attempts) + 1
