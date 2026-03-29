import logging
from random import choice

from sqlalchemy.orm import Session

from ..constants import CHANNEL, START_ROUND_FEATURE, ROUNDS
from app.round.exceptions import RoundError, StartRoundException

from ..data import save_round_start
from ..data.upsert_user_profile import upsert_user_profile
from ..models import RoundStartResponse
from ..types.args import StartRoundArgs

logger = logging.getLogger(__name__)


def start_round(session: Session, args: StartRoundArgs) -> RoundStartResponse:
    selected_round = choice(ROUNDS)
    target_image_url = f"/static/{selected_round['reference_image']}"

    try:
        upsert_user_profile(session, user_id=args.user_id, email=args.user_email, display_name=args.user_display_name)
        save_round_start(
            session=session,
            user_id=args.user_id,
            round_id=selected_round["id"],
            target_image_url=target_image_url,
        )
    except Exception as exc:
        logger.error(
            "Failed to start round",
            extra={"channel": CHANNEL, "feature": START_ROUND_FEATURE, "error": str(exc), "user": args.user_id},
        )
        raise StartRoundException(
            RoundError.SAVE_FAILED, message="Failed to start round",
        ) from exc

    logger.info(
        "Round started",
        extra={
            "channel": CHANNEL, "feature": START_ROUND_FEATURE,
            "user": args.user_id, "round_id": selected_round["id"],
        },
    )

    return RoundStartResponse(
        round_id=selected_round["id"],
        target_image_url=target_image_url,
    )
