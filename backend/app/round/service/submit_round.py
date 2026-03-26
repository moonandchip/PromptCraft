import logging
from pathlib import Path

from sqlalchemy.orm import Session

from ..constants import CHANNEL, SUBMIT_ROUND_FEATURE
from app.round.exceptions import RoundError, SubmitRoundException

from ..data import save_submission
from ..models import RoundSubmitResponse
from ..types.args import SubmitRoundArgs
from .get_round_by_id import get_round_by_id
from .clip_scoring import compute_similarity_score
from .generate_image import GenerationError, generate_image

logger = logging.getLogger(__name__)
_STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"


def submit_round(session: Session, args: SubmitRoundArgs) -> RoundSubmitResponse:
    matched_round = get_round_by_id(round_id=args.round_id)
    if matched_round is None:
        raise SubmitRoundException(
            RoundError.NOT_FOUND,
            message=f"Round '{args.round_id}' not found",
        )

    try:
        image_url = generate_image(args.user_prompt)
    except GenerationError as exc:
        error_code = RoundError.GENERATION_TIMEOUT if exc.status_code == 504 else RoundError.GENERATION_FAILED
        raise SubmitRoundException(
            error_code, message=exc.detail,
        ) from exc

    similarity_score = 0.0
    reference_path = _STATIC_DIR / matched_round["reference_image"]
    try:
        similarity_score = compute_similarity_score(
            reference_image_path=reference_path,
            generated_image_url=image_url,
        )
    except Exception as exc:
        logger.error(
            "CLIP scoring failed; returning score 0",
            extra={"channel": CHANNEL, "feature": SUBMIT_ROUND_FEATURE, "error": str(exc), "user": args.user_email},
        )

    try:
        save_submission(
            session=session,
            user_email=args.user_email,
            reference_image=matched_round["reference_image"],
            difficulty=matched_round["difficulty"],
            prompt_text=args.user_prompt,
            round_id=args.round_id,
            generated_image_url=image_url,
            similarity_score=similarity_score,
        )
    except Exception as exc:
        logger.error(
            "Failed to save round submission",
            extra={"channel": CHANNEL, "feature": SUBMIT_ROUND_FEATURE, "error": str(exc), "user": args.user_email},
        )
        raise SubmitRoundException(
            RoundError.SAVE_FAILED, message="Failed to save submission",
        ) from exc

    logger.info(
        "Round submitted successfully",
        extra={
            "channel": CHANNEL, "feature": SUBMIT_ROUND_FEATURE,
            "user": args.user_email, "round_id": args.round_id, "score": similarity_score,
        },
    )

    return RoundSubmitResponse(generated_image_url=image_url, similarity_score=similarity_score)
