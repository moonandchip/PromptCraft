import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .entities import RoundUser


def get_or_create_user(session: Session, email: str, username: str | None = None) -> str:
    """Returns a user ID for the provided email, creating the user if needed.

    Args:
        session: The SQLAlchemy session used for data access.
        email: The email address used to find or create the user.
        username: Optional username to store when creating the user.

    Returns:
        The ID of an existing or newly created user row.

    Raises:
        Exception: Propagates database errors raised by the session.
    """
    existing_user_id = session.execute(
        select(RoundUser.id).where(RoundUser.email == email).limit(1)
    ).scalar_one_or_none()
    if existing_user_id is not None:
        return str(existing_user_id)

    new_user = RoundUser(
        id=str(uuid.uuid4()),
        username=username or email.split("@")[0],
        email=email,
        password_hash="",
        total_score=0,
        role="user",
    )
    session.add(new_user)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        existing_user_id = session.execute(
            select(RoundUser.id).where(RoundUser.email == email).limit(1)
        ).scalar_one()
        return str(existing_user_id)

    return str(new_user.id)
