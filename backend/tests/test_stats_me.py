import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.auth.constants import ERR_MISSING_BEARER_TOKEN
from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.main import app
from app.stats.db import get_db_connection


def _build_connection(rows: list[tuple[str, float]]) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE rounds (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, score REAL NOT NULL)"
    )
    if rows:
        connection.executemany("INSERT INTO rounds (user_id, score) VALUES (?, ?)", rows)
    connection.commit()
    return connection


def test_stats_me_requires_bearer_token():
    client = TestClient(app)
    response = client.get("/stats/me")
    assert response.status_code == 401
    assert response.json()["detail"] == ERR_MISSING_BEARER_TOKEN


def test_stats_me_returns_aggregated_stats_for_authenticated_user():
    connection = _build_connection(
        [
            ("u1", 10),
            ("u1", 20),
            ("u1", 50),
            ("u2", 99),
        ]
    )
    client = TestClient(app)
    app.dependency_overrides[get_current_user] = lambda: UserResponse(
        id="u1",
        email="u1@example.com",
        name="User One",
    )
    app.dependency_overrides[get_db_connection] = lambda: connection

    response = client.get("/stats/me", headers={"Authorization": "Bearer test-token"})

    app.dependency_overrides.clear()
    connection.close()

    assert response.status_code == 200
    payload = response.json()
    assert payload["rounds_played"] == 3
    assert payload["best_score"] == 50.0
    assert payload["average_score"] == pytest.approx(26.6666667, rel=1e-6)


def test_stats_me_returns_zeros_for_user_with_no_rounds():
    connection = _build_connection([("u2", 42)])
    client = TestClient(app)
    app.dependency_overrides[get_current_user] = lambda: UserResponse(
        id="u1",
        email="u1@example.com",
        name="User One",
    )
    app.dependency_overrides[get_db_connection] = lambda: connection

    response = client.get("/stats/me", headers={"Authorization": "Bearer test-token"})

    app.dependency_overrides.clear()
    connection.close()

    assert response.status_code == 200
    assert response.json() == {
        "rounds_played": 0,
        "average_score": 0.0,
        "best_score": 0.0,
    }
