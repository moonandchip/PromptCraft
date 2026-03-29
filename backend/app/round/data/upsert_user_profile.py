from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .entities import UserProfile


def upsert_user_profile(
    session: Session,
    user_id: str,
    email: str,
    display_name: str | None = None,
) -> None:
    existing = session.get(UserProfile, user_id)
    if existing:
        existing.email = email
        existing.display_name = display_name or existing.display_name
        existing.last_seen_at = datetime.now(timezone.utc)
    else:
        profile = UserProfile(
            id=user_id,
            email=email,
            display_name=display_name,
        )
        session.add(profile)
    session.flush()
