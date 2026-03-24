import logging

from sqlalchemy.orm import Session

from app.constants import STATS_CHANNEL
from app.stats.domain.constants import GET_STATS_FEATURE
from app.stats.domain.exceptions import GetStatsException, StatsError

from app.stats.data import get_rounds_aggregates_by_user_id
from app.stats.models import StatsResponse

logger = logging.getLogger(__name__)


def get_user_stats(session: Session, user_id: str) -> StatsResponse:
    try:
        rounds_played, average_score, best_score = get_rounds_aggregates_by_user_id(
            session=session, user_id=user_id,
        )
    except Exception as exc:
        logger.exception(
            "Failed to get user stats",
            extra={"channel": STATS_CHANNEL, "feature": GET_STATS_FEATURE, "user": user_id},
        )
        raise GetStatsException(
            status_code=500, error_code=StatsError.UNKNOWN_ERROR, message="Failed to retrieve stats",
        ) from exc

    logger.info(
        "Stats retrieved",
        extra={"channel": STATS_CHANNEL, "feature": GET_STATS_FEATURE, "user": user_id},
    )

    return StatsResponse(
        rounds_played=rounds_played,
        average_score=average_score,
        best_score=best_score,
    )
