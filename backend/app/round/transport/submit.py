from fastapi import HTTPException, status

from ..constants import ERR_ROUND_NOT_FOUND, ROUNDS
from ..models import RoundInfo, SubmitRequest, SubmitResponse
from ..service.generate_image import GenerationError, generate_image


def get_rounds_endpoint() -> list[RoundInfo]:
    """Return all available practice rounds."""
    return [RoundInfo(**r) for r in ROUNDS]


def submit_endpoint(body: SubmitRequest) -> SubmitResponse:
    """Generate an AI image from the user prompt and return the URL."""
    # Validate the round exists
    round_ids = {r["id"] for r in ROUNDS}
    if body.round_id not in round_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERR_ROUND_NOT_FOUND)

    try:
        image_url = generate_image(body.user_prompt)
    except GenerationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    return SubmitResponse(generated_image_url=image_url, similarity_score=0.0)
