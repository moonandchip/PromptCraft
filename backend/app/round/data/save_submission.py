from sqlalchemy.orm import Session

from .get_or_create_image import get_or_create_image
from .get_or_create_user import get_or_create_user
from .save_attempt import save_attempt
from .save_prompt import save_prompt


def save_submission(
    session: Session,
    user_email: str,
    reference_image: str,
    difficulty: str,
    prompt_text: str,
    similarity_score: float,
) -> None:
    """Persists a complete round submission transaction.

    Args:
        session: The SQLAlchemy session used for data access.
        user_email: The email address of the authenticated user.
        reference_image: The reference image filename for the selected round.
        difficulty: The textual difficulty of the selected round.
        prompt_text: The user prompt text submitted for the round.
        similarity_score: The computed similarity score for the submission.

    Returns:
        None.

    Raises:
        Exception: Propagates database errors raised during persistence.
    """
    user_id = get_or_create_user(session=session, email=user_email)
    image_id = get_or_create_image(
        session=session,
        reference_image=reference_image,
        difficulty=difficulty,
    )
    prompt_id = save_prompt(
        session=session,
        user_id=user_id,
        image_id=image_id,
        prompt_text=prompt_text,
    )
    save_attempt(
        session=session,
        user_id=user_id,
        image_id=image_id,
        prompt_id=prompt_id,
        similarity_score=similarity_score,
    )
    session.commit()
