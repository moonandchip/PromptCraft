import logging

from sqlalchemy.orm import Session

from ..constants import CHANNEL, GET_STATS_FEATURE
from ..exceptions import GetStatsException, StatsError

from app.stats.data import get_user_stats_from_attempts
from app.stats.models import RecentAttempt, StatsResponse

logger = logging.getLogger(__name__)


def get_user_stats(session: Session, user_id: str) -> StatsResponse:
    try:
        raw = get_user_stats_from_attempts(session=session, user_id=user_id)
    except Exception as exc:
        logger.error(
            "Failed to get user stats",
            extra={"channel": CHANNEL, "feature": GET_STATS_FEATURE, "error": str(exc), "user": user_id},
        )
        raise GetStatsException(
            StatsError.UNKNOWN_ERROR, message="Failed to retrieve stats",
        ) from exc

    logger.info(
        "Stats retrieved",
        extra={"channel": CHANNEL, "feature": GET_STATS_FEATURE, "user": user_id},
    )

    return StatsResponse(
        total_rounds=raw["total_rounds"],
        total_attempts=raw["total_attempts"],
        average_score=raw["average_score"],
        best_score=raw["best_score"],
        recent_attempts=[RecentAttempt(**a) for a in raw["recent_attempts"]],
    )
