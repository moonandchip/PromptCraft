from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db import get_db_session as app_get_db_session


def get_db_session() -> Generator[Session, None, None]:
    """Provides a database session dependency for round transport handlers.

    Args:
        None.

    Returns:
        A generator that yields a SQLAlchemy session for a request lifecycle.

    Raises:
        Exception: Propagates errors raised by the shared app DB session provider.
    """
    yield from app_get_db_session()
