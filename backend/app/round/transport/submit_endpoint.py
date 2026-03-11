from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse

from ..models import SubmitRequest, SubmitResponse
from ..service import RoundServiceError, submit_round
from .get_db_session import get_db_session


def submit_endpoint(
    body: SubmitRequest,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> SubmitResponse:
    """Handles round submission for the authenticated user.

    Args:
        body: The validated submission request payload.
        current_user: The authenticated user submitting the prompt.
        session: The SQLAlchemy session used for persistence operations.

    Returns:
        A submission response with generated image URL and similarity score.

    Raises:
        HTTPException: If service-layer validation, generation, or persistence fails.
    """
    try:
        return submit_round(
            session=session,
            user_email=current_user.email,
            round_id=body.round_id,
            user_prompt=body.user_prompt,
        )
    except RoundServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
