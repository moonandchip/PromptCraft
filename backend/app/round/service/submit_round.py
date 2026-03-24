import logging
from pathlib import Path

from sqlalchemy.orm import Session

from app.constants import ROUND_CHANNEL
from app.round.constants import SUBMIT_ROUND_FEATURE
from app.round.exceptions import RoundError, SubmitRoundException

from ..data import save_submission
from ..models import RoundSubmitResponse
from .get_round_by_id import get_round_by_id
from .clip_scoring import compute_similarity_score
from .generate_image import GenerationError, generate_image

logger = logging.getLogger(__name__)
_STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"


def submit_round(session: Session, user_email: str, round_id: str, user_prompt: str) -> RoundSubmitResponse:
    matched_round = get_round_by_id(round_id=round_id)
    if matched_round is None:
        raise SubmitRoundException(
            status_code=404,
            error_code=RoundError.NOT_FOUND,
            message=f"Round '{round_id}' not found",
        )

    try:
        image_url = generate_image(user_prompt)
    except GenerationError as exc:
        error_code = RoundError.GENERATION_TIMEOUT if exc.status_code == 504 else RoundError.GENERATION_FAILED
        raise SubmitRoundException(
            status_code=exc.status_code, error_code=error_code, message=exc.detail,
        ) from exc

    similarity_score = 0.0
    reference_path = _STATIC_DIR / matched_round["reference_image"]
    try:
        similarity_score = compute_similarity_score(
            reference_image_path=reference_path,
            generated_image_url=image_url,
        )
    except Exception:
        logger.exception(
            "CLIP scoring failed; returning score 0",
            extra={"channel": ROUND_CHANNEL, "feature": SUBMIT_ROUND_FEATURE, "user": user_email},
        )

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
        logger.exception(
            "Failed to save round submission",
            extra={"channel": ROUND_CHANNEL, "feature": SUBMIT_ROUND_FEATURE, "user": user_email},
        )
        raise SubmitRoundException(
            status_code=500, error_code=RoundError.SAVE_FAILED, message="Failed to save submission",
        ) from exc

    logger.info(
        "Round submitted successfully",
        extra={
            "channel": ROUND_CHANNEL, "feature": SUBMIT_ROUND_FEATURE,
            "user": user_email, "round_id": round_id, "score": similarity_score,
        },
    )

    return RoundSubmitResponse(generated_image_url=image_url, similarity_score=similarity_score)
