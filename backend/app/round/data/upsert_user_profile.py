from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .entities import UserProfile
from sqlalchemy import select


def upsert_user_profile(
    session: Session,
    user_id: str,
    email: str,
    display_name: str | None = None,
) -> None:
    existing = session.execute(
        select(UserProfile).where(UserProfile.email == email)
    ).scalar_one_or_none()
    if existing:
        existing.display_name = display_name or existing.display_name
        existing.last_seen_at = datetime.now(timezone.utc)
        session.flush()
        return existing.id
    else:
        profile = UserProfile(
            id=user_id,
            email=email,
            display_name=display_name,
        )
        session.add(profile)
        session.flush()
        return profile.id
