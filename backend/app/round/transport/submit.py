import logging
from pathlib import Path

from fastapi import Depends, HTTPException, status

from ...auth.dependencies import get_current_user
from ...auth.models import UserResponse
from ...db import get_db_conn
from ..constants import ERR_ROUND_NOT_FOUND, ROUNDS
from ..data.save_submission import get_or_create_image, get_or_create_user, save_attempt, save_prompt
from ..models import RoundInfo, SubmitRequest, SubmitResponse
from ..service.clip_scoring import compute_similarity_score
from ..service.generate_image import GenerationError, generate_image

logger = logging.getLogger(__name__)

# Reference images live alongside the app package in app/static/
_STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"


def get_rounds_endpoint() -> list[RoundInfo]:
    """Return all available practice rounds."""
    return [RoundInfo(**r) for r in ROUNDS]


def _persist_submission(
    user_email: str,
    round_info: dict,
    user_prompt: str,
    similarity_score: float,
) -> None:
    """Save the prompt and attempt records to the database."""
    with get_db_conn() as conn:
        db_user_id = get_or_create_user(conn, email=user_email)
        db_image_id = get_or_create_image(
            conn,
            reference_image=round_info["reference_image"],
            difficulty=round_info["difficulty"],
        )
        prompt_id = save_prompt(
            conn,
            user_id=db_user_id,
            image_id=db_image_id,
            prompt_text=user_prompt,
        )
        save_attempt(
            conn,
            user_id=db_user_id,
            image_id=db_image_id,
            prompt_id=prompt_id,
            similarity_score=similarity_score,
        )


def submit_endpoint(
    body: SubmitRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> SubmitResponse:
    """Accept a user prompt, generate an AI image, persist the result, and return it."""
    # Validate the round exists
    matched_round = next((r for r in ROUNDS if r["id"] == body.round_id), None)
    if matched_round is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERR_ROUND_NOT_FOUND)

    try:
        image_url = generate_image(body.user_prompt)
    except GenerationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    # --- CLIP similarity scoring ---
    similarity_score = 0.0
    reference_path = _STATIC_DIR / matched_round["reference_image"]
    try:
        similarity_score = compute_similarity_score(
            reference_image_path=reference_path,
            generated_image_url=image_url,
        )
    except Exception:
        logger.exception("CLIP scoring failed – returning score 0")

    # --- Persist prompt and attempt to DB ---
    try:
        _persist_submission(
            user_email=current_user.email,
            round_info=matched_round,
            user_prompt=body.user_prompt,
            similarity_score=similarity_score,
        )
    except Exception:
        logger.exception("DB persistence failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save submission",
        )

    return SubmitResponse(generated_image_url=image_url, similarity_score=similarity_score)
