import logging
import os
from contextlib import contextmanager
from typing import Generator
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

import psycopg2

log = logging.getLogger(__name__)

_DATABASE_URL_ENV = "DATABASE_URL"


def _strip_schema_param(url: str) -> str:
    """Remove the Prisma-only 'schema' query parameter psycopg2 rejects."""
    parsed = urlparse(url)
    params = {k: v for k, v in parse_qs(parsed.query).items() if k != "schema"}
    clean_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=clean_query))


@contextmanager
def get_db_conn() -> Generator:
    """Yield a psycopg2 connection; commit on exit, rollback on error."""
    url = os.environ.get(_DATABASE_URL_ENV, "").strip()
    if not url:
        raise RuntimeError(f"{_DATABASE_URL_ENV} environment variable is not set")
    conn = psycopg2.connect(_strip_schema_param(url))
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
