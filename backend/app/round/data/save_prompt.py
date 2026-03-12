import uuid

from sqlalchemy.orm import Session

from .entities import Prompt


def save_prompt(session: Session, user_id: str, image_id: str, prompt_text: str) -> str:
    """Creates a prompt row for a user submission.

    Args:
        session: The SQLAlchemy session used for data access.
        user_id: The ID of the submitting user.
        image_id: The ID of the round reference image.
        prompt_text: The user prompt text submitted for the round.

    Returns:
        The ID of the newly created prompt row.

    Raises:
        Exception: Propagates database errors raised by the session.
    """
    prompt = Prompt(
        id=str(uuid.uuid4()),
        user_id=user_id,
        image_id=image_id,
        prompt_text=prompt_text,
    )
    session.add(prompt)
    session.flush()
    return str(prompt.id)
