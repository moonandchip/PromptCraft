from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from .entities import UserProfile


def upsert_user_profile(
    session: Session,
    user_id: str,
    email: str,
    display_name: str | None = None,
) -> str:
    """Inserts or updates a user_profile row keyed by `user_id`.

    Uses Postgres `INSERT ... ON CONFLICT (id) DO UPDATE` so concurrent
    requests for the same user can't race into a UniqueViolation. The
    `auth."User"` table is the source of truth for identity; this row is a
    cache and we always want the freshest values from the JWT.
    """
    now = datetime.now(timezone.utc)
    safe_display_name = display_name or email.split("@")[0]

    stmt = pg_insert(UserProfile).values(
        id=user_id,
        email=email,
        display_name=safe_display_name,
        created_at=now,
        last_seen_at=now,
    )

    # On conflict, refresh email + last_seen_at, and either fill in
    # display_name when it's empty or override it when an explicit one was
    # passed (matches the original "preserve existing if no new value" rule).
    update_values: dict = {
        "email": stmt.excluded.email,
        "last_seen_at": stmt.excluded.last_seen_at,
    }
    if display_name:
        update_values["display_name"] = display_name
    else:
        # COALESCE keeps a non-null existing display_name; falls back to the
        # safe default (email prefix) only when the existing row had none.
        update_values["display_name"] = func.coalesce(
            UserProfile.display_name, safe_display_name,
        )

    stmt = stmt.on_conflict_do_update(
        index_elements=[UserProfile.id],
        set_=update_values,
    ).returning(UserProfile.id)

    returned_id = session.execute(stmt).scalar_one()
    session.flush()
    return returned_id