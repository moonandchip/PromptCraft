from sqlalchemy import select
from sqlalchemy.orm import Session

from .entities import Attempt, Prompt


def get_attempts_by_round_id(
    session: Session,
    user_id: str,
    round_id: str,
) -> list[tuple[int, str, str, float]]:
    """Retrieves all user attempts for a round ordered by attempt number.

    Args:
        session: The SQLAlchemy session used for data access.
        user_id: The authenticated user ID.
        round_id: The round ID to retrieve attempts for.

    Returns:
        A list of tuples in the form:
        (attempt_number, prompt, generated_image_url, similarity_score).

    Raises:
        Exception: Propagates database errors raised by the session.
    """
    query = (
        select(
            Attempt.attempt_number.label("attempt_number"),
            Prompt.prompt_text.label("prompt"),
            Attempt.generated_image_url.label("generated_image_url"),
            Attempt.similarity_score.label("similarity_score"),
        )
        .join(Prompt, Prompt.id == Attempt.prompt_id)
        .where(
            Attempt.user_id == user_id,
            Attempt.round_id == round_id,
        )
        .order_by(Attempt.attempt_number.asc())
    )
    rows = session.execute(query).all()
    return [
        (
            int(row.attempt_number),
            str(row.prompt),
            str(row.generated_image_url),
            float(row.similarity_score or 0.0),
        )
        for row in rows
    ]
