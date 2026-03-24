import unittest
from unittest.mock import MagicMock

from app.stats.data.get_user_stats_from_attempts import get_user_stats_from_attempts


class TestGetUserStatsFromAttempts(unittest.TestCase):
    def test_returns_zeros_when_no_attempts(self):
        session = MagicMock()
        agg_row = MagicMock()
        agg_row.total_rounds = 0
        agg_row.total_attempts = 0
        agg_row.average_score = None
        agg_row.best_score = None

        session.execute.return_value.one.return_value = agg_row
        session.execute.return_value.all.return_value = []

        # Need to handle two calls: first .one() for agg, then .all() for recent
        call_count = [0]
        original_execute = session.execute

        def side_effect(query):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] == 1:
                result.one.return_value = agg_row
            else:
                result.all.return_value = []
            return result

        session.execute.side_effect = side_effect

        result = get_user_stats_from_attempts(session=session, user_id="u1")

        self.assertEqual(result["total_rounds"], 0)
        self.assertEqual(result["total_attempts"], 0)
        self.assertEqual(result["average_score"], 0.0)
        self.assertEqual(result["best_score"], 0.0)
        self.assertEqual(result["recent_attempts"], [])

    def test_returns_stats_with_recent_attempts(self):
        session = MagicMock()

        agg_row = MagicMock()
        agg_row.total_rounds = 2
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

        call_count = [0]

        def side_effect(query):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] == 1:
                result.one.return_value = agg_row
            else:
                result.all.return_value = [recent_row]
            return result

        session.execute.side_effect = side_effect

        result = get_user_stats_from_attempts(session=session, user_id="u1")

        self.assertEqual(result["total_rounds"], 2)
        self.assertEqual(result["total_attempts"], 5)
        self.assertEqual(result["average_score"], 45.6)
        self.assertEqual(result["best_score"], 80.0)
        self.assertEqual(len(result["recent_attempts"]), 1)
        self.assertEqual(result["recent_attempts"][0]["round_id"], "ancient-temple")
        self.assertEqual(result["recent_attempts"][0]["similarity_score"], 80.0)
