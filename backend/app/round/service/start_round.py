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

_VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def _select_round(difficulty: str | None) -> dict:
    if difficulty and difficulty.lower() in _VALID_DIFFICULTIES:
        candidates = [r for r in ROUNDS if r["difficulty"] == difficulty.lower()]
        if candidates:
            return choice(candidates)
    return choice(ROUNDS)


def start_round(session: Session, args: StartRoundArgs) -> RoundStartResponse:
    selected_round = _select_round(args.difficulty)
    target_image_url = f"/static/{selected_round['reference_image']}"

    try:
        actual_user_id = upsert_user_profile(
            session,
            user_id=args.user_id,
            email=args.user_email,
            display_name=args.user_display_name,
        )

        save_round_start(
            session=session,
            user_id=actual_user_id,
            round_id=selected_round["id"],
            target_image_url=target_image_url,
        )
    except Exception as exc:
        logger.exception(
            "Failed to start round",
            extra={
                "channel": CHANNEL,
                "feature": START_ROUND_FEATURE,
                "error": str(exc),
                "user": args.user_id,
            },
        )
        raise StartRoundException(
            RoundError.SAVE_FAILED, message="Failed to start round",
        ) from exc

    logger.info(
        "Round started",
        extra={
            "channel": CHANNEL,
            "feature": START_ROUND_FEATURE,
            "user": actual_user_id,
            "round_id": selected_round["id"],
        },
    )

    return RoundStartResponse(
        round_id=selected_round["id"],
        target_image_url=target_image_url,
        title=selected_round["title"],
        difficulty=selected_round["difficulty"],
        target_prompt=selected_round.get("target_prompt", ""),
    )