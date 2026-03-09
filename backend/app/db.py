import os
from collections.abc import Generator
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Shared SQLAlchemy declarative base for ORM models."""

_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def _normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def _strip_schema_query(database_url: str) -> tuple[str, str | None]:
    parsed = urlparse(database_url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    schema = params.pop("schema", [None])[0]
    query = urlencode(params, doseq=True)
    rebuilt = parsed._replace(query=query)
    return urlunparse(rebuilt), schema


def get_engine() -> Engine:
    global _engine
    if _engine is not None:
        return _engine

    raw_database_url = os.getenv("DATABASE_URL", "").strip()
    if not raw_database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    normalized_url = _normalize_database_url(raw_database_url)
    database_url, schema = _strip_schema_query(normalized_url)

    engine_kwargs: dict[str, object] = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    elif schema:
        engine_kwargs["connect_args"] = {"options": f"-c search_path={schema}"}

    _engine = create_engine(database_url, **engine_kwargs)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)
    return _session_factory


def get_db_session() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def dispose_engine() -> None:
    global _engine, _session_factory
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_factory = None
