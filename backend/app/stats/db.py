import os
import sqlite3
from collections.abc import Generator
from urllib.parse import parse_qs, urlparse, urlunparse


def _strip_query_params(database_url: str) -> str:
    parsed = urlparse(database_url)
    clean_url = parsed._replace(query="")
    return urlunparse(clean_url)


def _get_sqlite_path(database_url: str) -> str:
    if database_url.startswith("sqlite:///"):
        return database_url.replace("sqlite:///", "", 1)
    if database_url.startswith("sqlite://"):
        return database_url.replace("sqlite://", "", 1)
    raise RuntimeError("Unsupported SQLite URL format. Use sqlite:///path/to/db.sqlite3")


def _connect_postgres(database_url: str):
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("Postgres DATABASE_URL requires 'psycopg' to be installed.") from exc

    # Strip query params such as ?schema=public so psycopg can connect directly.
    base_url = _strip_query_params(database_url)
    options = parse_qs(urlparse(database_url).query)
    search_path = options.get("schema", [None])[0]
    if search_path:
        return psycopg.connect(base_url, options=f"-c search_path={search_path}")
    return psycopg.connect(base_url)


def create_db_connection():
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    if database_url.startswith(("postgresql://", "postgres://")):
        return _connect_postgres(database_url)

    if database_url.startswith("sqlite://"):
        sqlite_path = _get_sqlite_path(database_url)
        return sqlite3.connect(sqlite_path)

    raise RuntimeError("Unsupported DATABASE_URL. Expected postgresql:// or sqlite://")


def get_db_connection() -> Generator[object, None, None]:
    connection = create_db_connection()
    try:
        yield connection
    finally:
        connection.close()
