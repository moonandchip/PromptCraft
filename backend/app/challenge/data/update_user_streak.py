from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.round.data.entities import UserProfile


def update_user_streak(session: Session, user_id: str, today: date) -> tuple[int, int]:
    """Increments / resets the user's daily-challenge streak based on `today`.

    Rules:
      - First-ever play: streak = 1.
      - Already played today: streak unchanged (idempotent within the day).
      - Played yesterday: streak += 1.
      - Otherwise (gap of ≥1 day): streak resets to 1.

    Updates `current_streak`, `longest_streak`, and `last_played_date` on the
    profile. Caller owns the transaction.

    Returns: (current_streak, longest_streak) after the update.
    """
    profile = session.get(UserProfile, user_id)
    if profile is None:
        # Should never happen — submit_challenge upserts the profile first.
        # Be defensive: skip rather than blow up the submission.
        return (0, 0)

    last = profile.last_played_date
    if last == today:
        return (profile.current_streak, profile.longest_streak)

    if last is not None and last == today - timedelta(days=1):
        profile.current_streak = (profile.current_streak or 0) + 1
    else:
        profile.current_streak = 1

    if profile.current_streak > (profile.longest_streak or 0):
        profile.longest_streak = profile.current_streak
    profile.last_played_date = today

    session.flush()
    return (profile.current_streak, profile.longest_streak)
