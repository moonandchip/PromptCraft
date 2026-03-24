import unittest
from unittest.mock import create_autospec, patch

from sqlalchemy.orm import Session

from app.stats.models import StatsResponse
from app.stats.service.get_user_stats import get_user_stats


class TestGetUserStats(unittest.TestCase):
    @patch("app.stats.service.get_user_stats.get_user_stats_from_attempts", autospec=True)
    def test_maps_data_into_response_model(self, mock_data):
        session = create_autospec(Session, instance=True, spec_set=True)
        mock_data.return_value = {
            "total_rounds": 3,
            "total_attempts": 7,
            "average_score": 26.7,
            "best_score": 50.0,
            "recent_attempts": [
                {
                    "round_id": "ancient-temple",
                    "attempt_number": 1,
                    "prompt": "a temple",
                    "generated_image_url": "https://example.com/img.png",
                    "similarity_score": 50.0,
                    "created_at": "2026-03-01T12:00:00",
                },
            ],
        }

        stats = get_user_stats(session=session, user_id="u1")

        self.assertIsInstance(stats, StatsResponse)
        self.assertEqual(stats.total_rounds, 3)
        self.assertEqual(stats.total_attempts, 7)
        self.assertAlmostEqual(stats.average_score, 26.7)
        self.assertEqual(stats.best_score, 50.0)
        self.assertEqual(len(stats.recent_attempts), 1)
        self.assertEqual(stats.recent_attempts[0].round_id, "ancient-temple")
        self.assertEqual(stats.recent_attempts[0].similarity_score, 50.0)
        mock_data.assert_called_once_with(session=session, user_id="u1")

    @patch("app.stats.service.get_user_stats.get_user_stats_from_attempts", autospec=True)
    def test_empty_stats_for_new_user(self, mock_data):
        session = create_autospec(Session, instance=True, spec_set=True)
        mock_data.return_value = {
            "total_rounds": 0,
            "total_attempts": 0,
            "average_score": 0.0,
            "best_score": 0.0,
            "recent_attempts": [],
        }

        stats = get_user_stats(session=session, user_id="new-user")

        self.assertEqual(stats.total_rounds, 0)
        self.assertEqual(stats.total_attempts, 0)
        self.assertEqual(stats.recent_attempts, [])
