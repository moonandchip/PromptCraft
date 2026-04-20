import uuid

from sqlalchemy.orm import Session

from .entities import Attempt
from .get_next_attempt_number import get_next_attempt_number


def save_attempt(
    session: Session,
    user_id: str,
    image_id: str,
    prompt_id: str,
    round_id: str,
    generated_image_url: str,
    similarity_score: float,
    challenge_id: str | None = None,
) -> str:
    """Creates an attempt row for a submission.

    Args:
        session: The SQLAlchemy session used for data access.
        user_id: The ID of the user attempting the round.
        image_id: The ID of the reference image for the round.
        prompt_id: The ID of the prompt associated with this attempt.
        round_id: The static round identifier (e.g. "ancient-temple").
        generated_image_url: The URL of the AI-generated image for this attempt.
        similarity_score: The computed similarity score for this attempt.

    Returns:
        The ID of the newly created attempt row.

    Raises:
        Exception: Propagates database errors raised by the session.
    """
    attempt = Attempt(
        id=str(uuid.uuid4()),
        user_id=user_id,
        image_id=image_id,
        prompt_id=prompt_id,
        round_id=round_id,
        challenge_id=challenge_id,
        generated_image_url=generated_image_url,
        similarity_score=similarity_score,
        time_taken=0,
        attempt_number=get_next_attempt_number(session=session, user_id=user_id, round_id=round_id),
    )
    session.add(attempt)
    session.flush()
    return str(attempt.id)
