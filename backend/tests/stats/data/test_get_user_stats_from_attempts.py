import unittest
from unittest.mock import MagicMock

from app.stats.data.get_user_stats_from_attempts import get_user_stats_from_attempts


def _make_session(agg_row, practice_rounds, challenge_rounds, recent_rows):
    """Returns a MagicMock session whose execute() returns, in order:
    (1) agg query .one() -> agg_row
    (2) practice_rounds .scalar() -> int
    (3) challenge_rounds .scalar() -> int
    (4) recent query .all() -> list of rows
    """
    session = MagicMock()
    call_count = [0]

    def side_effect(query):
        call_count[0] += 1
        result = MagicMock()
        if call_count[0] == 1:
            result.one.return_value = agg_row
        elif call_count[0] == 2:
            result.scalar.return_value = practice_rounds
        elif call_count[0] == 3:
            result.scalar.return_value = challenge_rounds
        else:
            result.all.return_value = recent_rows
        return result

    session.execute.side_effect = side_effect
    return session


class TestGetUserStatsFromAttempts(unittest.TestCase):
    def test_returns_zeros_when_no_attempts(self):
        agg_row = MagicMock()
        agg_row.total_attempts = 0
        agg_row.average_score = None
        agg_row.best_score = None

        session = _make_session(agg_row, practice_rounds=0, challenge_rounds=0, recent_rows=[])

        result = get_user_stats_from_attempts(session=session, user_id="u1")

        self.assertEqual(result["total_rounds"], 0)
        self.assertEqual(result["total_attempts"], 0)
        self.assertEqual(result["average_score"], 0.0)
        self.assertEqual(result["best_score"], 0.0)
        self.assertEqual(result["recent_attempts"], [])

    def test_returns_stats_with_recent_attempts(self):
        agg_row = MagicMock()
        agg_row.total_attempts = 5
        agg_row.average_score = 45.6
        agg_row.best_score = 80.0

        recent_row = MagicMock()
        recent_row.round_id = "ancient-temple"
        recent_row.attempt_number = 3
        recent_row.prompt = "a temple"
        recent_row.generated_image_url = "https://example.com/img.png"
        recent_row.similarity_score = 80.0
        recent_row.created_at = MagicMock()
        recent_row.created_at.isoformat.return_value = "2026-03-01T12:00:00"

        session = _make_session(agg_row, practice_rounds=1, challenge_rounds=1, recent_rows=[recent_row])

        result = get_user_stats_from_attempts(session=session, user_id="u1")

        self.assertEqual(result["total_rounds"], 2)
        self.assertEqual(result["total_attempts"], 5)
        self.assertEqual(result["average_score"], 45.6)
        self.assertEqual(result["best_score"], 80.0)
        self.assertEqual(len(result["recent_attempts"]), 1)
        self.assertEqual(result["recent_attempts"][0]["round_id"], "ancient-temple")
        self.assertEqual(result["recent_attempts"][0]["similarity_score"], 80.0)

    def test_rounds_played_sums_practice_and_challenge(self):
        agg_row = MagicMock()
        agg_row.total_attempts = 25
        agg_row.average_score = 60.0
        agg_row.best_score = 90.0

        session = _make_session(agg_row, practice_rounds=7, challenge_rounds=10, recent_rows=[])

        result = get_user_stats_from_attempts(session=session, user_id="u1")

        self.assertEqual(result["total_rounds"], 17)
        self.assertEqual(result["total_attempts"], 25)

    def test_rounds_played_does_not_cap_at_unique_round_slugs(self):
        """Regression: previously total_rounds = COUNT(DISTINCT Attempt.round_id),
        which capped at the number of round slugs played instead of counting
        actual play sessions. A user who plays the same daily challenge 10 times
        should see 10 rounds, not 1."""
        agg_row = MagicMock()
        agg_row.total_attempts = 30
        agg_row.average_score = 50.0
        agg_row.best_score = 85.0

        session = _make_session(agg_row, practice_rounds=0, challenge_rounds=10, recent_rows=[])

        result = get_user_stats_from_attempts(session=session, user_id="u1")

        self.assertEqual(result["total_rounds"], 10)
