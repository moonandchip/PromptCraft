import logging
from pathlib import Path

from fastapi import HTTPException, status

from ..constants import ERR_ROUND_NOT_FOUND, ROUNDS
from ..models import RoundInfo, SubmitRequest, SubmitResponse
from ..service.clip_scoring import compute_similarity_score
from ..service.generate_image import GenerationError, generate_image

logger = logging.getLogger(__name__)

# Reference images live alongside the app package in app/static/
_STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"


def get_rounds_endpoint() -> list[RoundInfo]:
    """Return all available practice rounds."""
    return [RoundInfo(**r) for r in ROUNDS]


def submit_endpoint(body: SubmitRequest) -> SubmitResponse:
    """Generate an AI image from the user prompt, score it, and return both."""
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

    return SubmitResponse(generated_image_url=image_url, similarity_score=similarity_score)
