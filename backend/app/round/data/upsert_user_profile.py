from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select

from .entities import UserProfile


def upsert_user_profile(
    session: Session,
    user_id: str,
    email: str,
    display_name: str | None = None,
) -> str:
    safe_display_name = display_name or email.split("@")[0]

    # 🔥 NEW: check by email FIRST
    existing_by_email = session.execute(
        select(UserProfile).where(UserProfile.email == email)
    ).scalar_one_or_none()

    if existing_by_email:
        existing_by_email.last_seen_at = datetime.now(timezone.utc)

        if not existing_by_email.display_name:
            existing_by_email.display_name = safe_display_name
        elif display_name:
            existing_by_email.display_name = display_name

        session.flush()
        return existing_by_email.id

    # fallback: check by id (optional but safe)
    existing = session.get(UserProfile, user_id)

    if existing:
        existing.email = email
        existing.last_seen_at = datetime.now(timezone.utc)

        if not existing.display_name:
            existing.display_name = safe_display_name
        elif display_name:
            existing.display_name = display_name

        session.flush()
        return existing.id

    # create new
    profile = UserProfile(
        id=user_id,
        email=email,
        display_name=safe_display_name,
    )
    session.add(profile)
    session.flush()
    return profile.id