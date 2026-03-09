import unittest
from unittest.mock import create_autospec, patch

from sqlalchemy.orm import Session

from app.stats.models import StatsResponse
from app.stats.service.get_user_stats import get_user_stats


class TestGetUserStats(unittest.TestCase):
    @patch("app.stats.service.get_user_stats.get_rounds_aggregates_by_user_id", autospec=True)
    def test_maps_data_aggregates_into_response_model(self, mock_get_rounds_aggregates_by_user_id):
        session = create_autospec(Session, instance=True, spec_set=True)
        mock_get_rounds_aggregates_by_user_id.return_value = (3, 26.6666667, 50.0)

        stats = get_user_stats(session=session, user_id="u1")

        self.assertIsInstance(stats, StatsResponse)
        self.assertEqual(stats.rounds_played, 3)
        self.assertEqual(stats.best_score, 50.0)
        self.assertAlmostEqual(stats.average_score, 26.6666667)
        mock_get_rounds_aggregates_by_user_id.assert_called_once_with(session=session, user_id="u1")
