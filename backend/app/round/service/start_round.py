from random import choice

from sqlalchemy.orm import Session

from ..constants import ROUNDS
from ..data import save_round_start
from ..models import StartRoundResponse
from .errors import RoundServiceError


def start_round(session: Session, user_id: str) -> StartRoundResponse:
    """Starts a new practice round for an authenticated user.

    Args:
        session: The SQLAlchemy session used for persistence operations.
        user_id: The authenticated user ID starting the round.

    Returns:
        A start-round response containing round ID and target image URL.

    Raises:
        RoundServiceError: If saving the new round start record fails.
    """
    selected_round = choice(ROUNDS)
    target_image_url = f"/static/{selected_round['reference_image']}"

    try:
        save_round_start(
            session=session,
            user_id=user_id,
            round_id=selected_round["id"],
            target_image_url=target_image_url,
        )
    except Exception as exc:
        raise RoundServiceError(status_code=500, detail="Failed to start round") from exc

    return StartRoundResponse(
        round_id=selected_round["id"],
        target_image_url=target_image_url,
    )
