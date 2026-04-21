from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db import get_db_session as app_get_db_session


def get_db_session() -> Generator[Session, None, None]:
    yield from app_get_db_session()
