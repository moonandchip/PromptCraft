from sqlalchemy.orm import Session

from .get_or_create_image import get_or_create_image
from .save_attempt import save_attempt
from .save_prompt import save_prompt


def save_submission(
    session: Session,
    user_id: str,
    reference_image: str,
    difficulty: str,
    prompt_text: str,
    round_id: str,
    generated_image_url: str,
    similarity_score: float,
) -> None:
    """Stages image, prompt, and attempt rows for a round submission.

    Caller owns the transaction (commit/rollback); this function only
    delegates to the per-entity stagers.
    """
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
        round_id=round_id,
        generated_image_url=generated_image_url,
        similarity_score=similarity_score,
    )
