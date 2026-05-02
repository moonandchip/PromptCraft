from sqlalchemy.orm import Session

from app.round.data.entities import UserProfile


def get_user_streak(session: Session, user_id: str) -> tuple[int, int]:
    """Returns (current_streak, longest_streak) for the user, defaulting to
    (0, 0) when the profile hasn't been created yet."""
    profile = session.get(UserProfile, user_id)
    if profile is None:
        return (0, 0)
    return (profile.current_streak or 0, profile.longest_streak or 0)
