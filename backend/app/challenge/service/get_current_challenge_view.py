import logging

from sqlalchemy.orm import Session

from app.round.constants import ROUNDS
from app.round.service.get_round_by_id import get_round_by_id

from ..constants import CHANNEL, GET_CURRENT_FEATURE
from ..data import get_user_challenge_progress
from ..exceptions import ChallengeError, GetCurrentChallengeException
from ..models import ChallengeStateResponse
from ..types.args import GetCurrentChallengeArgs
from .get_or_create_current_challenge import get_or_create_current_challenge

logger = logging.getLogger(__name__)
_ROUNDS_BY_ID = {r["id"]: r for r in ROUNDS}


def get_current_challenge_view(session: Session, args: GetCurrentChallengeArgs) -> ChallengeStateResponse:
    challenge = get_or_create_current_challenge(session=session)

    round_info = get_round_by_id(round_id=challenge.round_id) or _ROUNDS_BY_ID.get(challenge.round_id)
    if round_info is None:
        logger.error(
            "Challenge references unknown round",
            extra={"channel": CHANNEL, "feature": GET_CURRENT_FEATURE, "round_id": challenge.round_id},
        )
        raise GetCurrentChallengeException(
            ChallengeError.NOT_FOUND, message="Challenge round is not configured",
        )

    attempts_used, best_score = get_user_challenge_progress(
        session=session, user_id=args.user_id, challenge_id=str(challenge.id),
    )

    return ChallengeStateResponse(
        challenge_id=str(challenge.id),
        period_type=challenge.period_type,
        period_end=challenge.period_end.isoformat(),
        round_id=challenge.round_id,
        title=round_info["title"],
        difficulty=round_info["difficulty"],
        target_image_url=f"/static/{round_info['reference_image']}",
        max_attempts=challenge.max_attempts,
        attempts_used=attempts_used,
        best_score=best_score,
    )
