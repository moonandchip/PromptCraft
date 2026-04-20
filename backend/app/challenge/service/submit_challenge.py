import logging
from pathlib import Path

from sqlalchemy.orm import Session

from app.round.data import get_or_create_image, save_attempt, save_prompt
from app.round.data.upsert_user_profile import upsert_user_profile
from app.round.service.clip_scoring import compute_similarity_score
from app.round.service.generate_image import GenerationError, generate_image
from app.round.service.get_round_by_id import get_round_by_id

from ..constants import CHANNEL, SUBMIT_CHALLENGE_FEATURE
from ..data import get_user_challenge_progress
from ..exceptions import ChallengeError, SubmitChallengeException
from ..models import ChallengeSubmitResponse
from ..types.args import SubmitChallengeArgs
from .get_or_create_current_challenge import get_or_create_current_challenge

logger = logging.getLogger(__name__)
_STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"


def submit_challenge(session: Session, args: SubmitChallengeArgs) -> ChallengeSubmitResponse:
    challenge = get_or_create_current_challenge(session=session)
    challenge_id = str(challenge.id)

    matched_round = get_round_by_id(round_id=challenge.round_id)
    if matched_round is None:
        raise SubmitChallengeException(
            ChallengeError.NOT_FOUND,
            message=f"Round '{challenge.round_id}' not found",
        )

    attempts_used, _best_so_far = get_user_challenge_progress(
        session=session, user_id=args.user_id, challenge_id=challenge_id,
    )
    if attempts_used >= challenge.max_attempts:
        raise SubmitChallengeException(
            ChallengeError.ATTEMPT_LIMIT_REACHED,
            message=f"Daily attempt limit of {challenge.max_attempts} reached",
        )

    try:
        image_url = generate_image(args.user_prompt)
    except GenerationError as exc:
        error_code = ChallengeError.GENERATION_TIMEOUT if exc.status_code == 504 else ChallengeError.GENERATION_FAILED
        raise SubmitChallengeException(error_code, message=exc.detail) from exc

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
            extra={"channel": CHANNEL, "feature": SUBMIT_CHALLENGE_FEATURE, "error": str(exc), "user": args.user_email},
        )

    try:
        upsert_user_profile(session, user_id=args.user_id, email=args.user_email, display_name=args.user_display_name)
        image_id = get_or_create_image(
            session=session,
            reference_image=matched_round["reference_image"],
            difficulty=matched_round["difficulty"],
        )
        prompt_id = save_prompt(
            session=session,
            user_id=args.user_id,
            image_id=image_id,
            prompt_text=args.user_prompt,
        )
        save_attempt(
            session=session,
            user_id=args.user_id,
            image_id=image_id,
            prompt_id=prompt_id,
            round_id=challenge.round_id,
            generated_image_url=image_url,
            similarity_score=similarity_score,
            challenge_id=challenge_id,
        )
        session.commit()
    except Exception as exc:
        session.rollback()
        logger.error(
            "Failed to save challenge submission",
            extra={"channel": CHANNEL, "feature": SUBMIT_CHALLENGE_FEATURE, "error": str(exc), "user": args.user_email},
        )
        raise SubmitChallengeException(
            ChallengeError.SAVE_FAILED, message="Failed to save submission",
        ) from exc

    attempts_used, best_score = get_user_challenge_progress(
        session=session, user_id=args.user_id, challenge_id=challenge_id,
    )

    logger.info(
        "Challenge submission saved",
        extra={
            "channel": CHANNEL,
            "feature": SUBMIT_CHALLENGE_FEATURE,
            "user": args.user_email,
            "challenge_id": challenge_id,
            "score": similarity_score,
        },
    )

    return ChallengeSubmitResponse(
        generated_image_url=image_url,
        similarity_score=similarity_score,
        attempts_used=attempts_used,
        attempts_remaining=max(challenge.max_attempts - attempts_used, 0),
        best_score=best_score,
    )
