import logging
from random import choice

from sqlalchemy.orm import Session

from app.constants import ROUND_CHANNEL
from app.round.constants import START_ROUND_FEATURE
from app.round.exceptions import RoundError, StartRoundException

from ..constants import ROUNDS
from ..data import save_round_start
from ..models import RoundStartResponse

logger = logging.getLogger(__name__)


def start_round(session: Session, user_id: str) -> RoundStartResponse:
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
        logger.exception(
            "Failed to start round",
            extra={"channel": ROUND_CHANNEL, "feature": START_ROUND_FEATURE, "user": user_id},
        )
        raise StartRoundException(
            status_code=500, error_code=RoundError.SAVE_FAILED, message="Failed to start round",
        ) from exc

    logger.info(
        "Round started",
        extra={
            "channel": ROUND_CHANNEL, "feature": START_ROUND_FEATURE,
            "user": user_id, "round_id": selected_round["id"],
        },
    )

    return RoundStartResponse(
        round_id=selected_round["id"],
        target_image_url=target_image_url,
    )
