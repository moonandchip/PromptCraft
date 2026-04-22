import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.challenge.data.get_leaderboard import get_leaderboard


class TestGetLeaderboard(unittest.TestCase):
    def _row(self, user_id, display_name, email, best_score, attempts_used):
        return SimpleNamespace(
            user_id=user_id,
            display_name=display_name,
            email=email,
            best_score=best_score,
            attempts_used=attempts_used,
        )

    def test_returns_tuples_with_display_name(self):
        session = MagicMock()
        session.execute.return_value.all.return_value = [
            self._row("u1", "Alice", "alice@example.com", 90.0, 2),
            self._row("u2", "Bob", "bob@example.com", 80.0, 1),
        ]

        rows = get_leaderboard(session=session, challenge_id="c-1", limit=10)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("u1", "Alice", 90.0, 2))
        self.assertEqual(rows[1], ("u2", "Bob", 80.0, 1))

    def test_falls_back_to_email_prefix_when_display_name_missing(self):
        session = MagicMock()
        session.execute.return_value.all.return_value = [
            self._row("u1", None, "anon42@example.com", 75.0, 1),
        ]

        rows = get_leaderboard(session=session, challenge_id="c-1", limit=10)

        self.assertEqual(rows[0][1], "anon42")

    def test_falls_back_to_anonymous_when_no_email(self):
        session = MagicMock()
        session.execute.return_value.all.return_value = [
            self._row("u1", None, None, 50.0, 1),
        ]

        rows = get_leaderboard(session=session, challenge_id="c-1", limit=10)

        self.assertEqual(rows[0][1], "anonymous")

    def test_handles_null_aggregates(self):
        session = MagicMock()
        session.execute.return_value.all.return_value = [
            self._row("u1", "Alice", "alice@example.com", None, None),
        ]

        rows = get_leaderboard(session=session, challenge_id="c-1", limit=10)

        self.assertEqual(rows[0][2], 0.0)
        self.assertEqual(rows[0][3], 0)

    def test_returns_empty_when_no_rows(self):
        session = MagicMock()
        session.execute.return_value.all.return_value = []

        rows = get_leaderboard(session=session, challenge_id="c-1", limit=10)

        self.assertEqual(rows, [])
