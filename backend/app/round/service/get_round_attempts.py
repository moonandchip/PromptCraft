from sqlalchemy.orm import Session

from ..data import get_attempts_by_round_id
from ..models import RoundAttemptResponse


def get_round_attempts(session: Session, user_id: str, round_id: str) -> list[RoundAttemptResponse]:
    """Returns all attempts for a user and round ordered by attempt number.

    Args:
        session: The SQLAlchemy session used for persistence operations.
        user_id: The authenticated user ID.
        round_id: The round ID whose attempts are requested.

    Returns:
        A list of attempts for the round ordered ascending by attempt number.

    Raises:
        Exception: Propagates data-layer errors.
    """
    attempts = get_attempts_by_round_id(session=session, user_id=user_id, round_id=round_id)
    return [
        RoundAttemptResponse(
            attempt_number=attempt_number,
            prompt=prompt,
            generated_image_url=generated_image_url,
            similarity_score=similarity_score,
        )
        for attempt_number, prompt, generated_image_url, similarity_score in attempts
    ]
