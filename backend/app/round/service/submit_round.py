import logging
from pathlib import Path

from sqlalchemy.orm import Session

from ..constants import ERR_ROUND_NOT_FOUND
from ..data import save_submission
from ..models import SubmitResponse
from .errors import RoundServiceError
from .get_round_by_id import get_round_by_id
from .clip_scoring import compute_similarity_score
from .generate_image import GenerationError, generate_image

logger = logging.getLogger(__name__)
_STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"


def submit_round(session: Session, user_email: str, round_id: str, user_prompt: str) -> SubmitResponse:
    """Processes a round submission and returns generated output with score.

    Args:
        session: The SQLAlchemy session used for persistence operations.
        user_email: The authenticated user email for this submission.
        round_id: The selected round ID.
        user_prompt: The prompt text submitted by the user.

    Returns:
        A submission response with generated image URL and similarity score.

    Raises:
        RoundServiceError: If the round is invalid, generation fails, or persistence fails.
    """
    matched_round = get_round_by_id(round_id=round_id)
    if matched_round is None:
        raise RoundServiceError(status_code=404, detail=ERR_ROUND_NOT_FOUND)

    try:
        image_url = generate_image(user_prompt)
    except GenerationError as exc:
        raise RoundServiceError(status_code=exc.status_code, detail=exc.detail) from exc

    similarity_score = 0.0
    reference_path = _STATIC_DIR / matched_round["reference_image"]
    try:
        similarity_score = compute_similarity_score(
            reference_image_path=reference_path,
            generated_image_url=image_url,
        )
    except Exception:
        logger.exception("CLIP scoring failed; returning score 0")

    try:
        save_submission(
            session=session,
            user_email=user_email,
            reference_image=matched_round["reference_image"],
            difficulty=matched_round["difficulty"],
            prompt_text=user_prompt,
            round_id=round_id,
            generated_image_url=image_url,
            similarity_score=similarity_score,
        )
    except Exception as exc:
        logger.exception("Failed to save round submission")
        raise RoundServiceError(status_code=500, detail="Failed to save submission") from exc

    return SubmitResponse(generated_image_url=image_url, similarity_score=similarity_score)
