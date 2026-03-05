import sqlite3

import pytest

from app.stats.service import get_user_stats


def _connection_with_rounds(rows: list[tuple[str, float]]) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE rounds (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, score REAL NOT NULL)"
    )
    if rows:
        connection.executemany("INSERT INTO rounds (user_id, score) VALUES (?, ?)", rows)
    connection.commit()
    return connection


def test_get_user_stats_returns_expected_aggregates():
    connection = _connection_with_rounds(
        [
            ("u1", 15),
            ("u1", 25),
            ("u1", 35),
            ("u2", 100),
        ]
    )
    stats = get_user_stats(connection=connection, user_id="u1")
    connection.close()

    assert stats.rounds_played == 3
    assert stats.best_score == 35.0
    assert stats.average_score == pytest.approx(25.0)


def test_get_user_stats_returns_zero_values_when_user_has_no_rounds():
    connection = _connection_with_rounds([("u2", 100)])
    stats = get_user_stats(connection=connection, user_id="u1")
    connection.close()

    assert stats.rounds_played == 0
    assert stats.average_score == 0.0
    assert stats.best_score == 0.0
