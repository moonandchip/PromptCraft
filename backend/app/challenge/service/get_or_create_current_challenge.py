from datetime import datetime, time, timedelta, timezone

from sqlalchemy.orm import Session

from app.round.constants import ROUNDS

from ..constants import DEFAULT_MAX_ATTEMPTS, PERIOD_DAILY
from ..data import create_challenge, get_active_challenge
from ..data.entities import Challenge


def _utc_day_bounds(now: datetime) -> tuple[datetime, datetime]:
    start = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
    return start, start + timedelta(days=1)


def _select_round_id_for_date(day: datetime) -> str:
    if not ROUNDS:
        raise RuntimeError("No practice rounds are configured")
    index = day.toordinal() % len(ROUNDS)
    return ROUNDS[index]["id"]


def get_or_create_current_challenge(session: Session, period_type: str = PERIOD_DAILY) -> Challenge:
    """Returns the active challenge for the period, creating it lazily.

    Daily challenges rotate based on the UTC date so all users see the same
    target image on a given day without requiring a scheduled job.
    """
    now = datetime.now(timezone.utc)
    existing = get_active_challenge(session=session, period_type=period_type, now=now)
    if existing is not None:
        return existing

    period_start, period_end = _utc_day_bounds(now)
    round_id = _select_round_id_for_date(period_start)
    return create_challenge(
        session=session,
        period_type=period_type,
        period_start=period_start,
        period_end=period_end,
        round_id=round_id,
        max_attempts=DEFAULT_MAX_ATTEMPTS,
    )
