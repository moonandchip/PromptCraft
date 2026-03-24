import unittest
from unittest.mock import MagicMock, patch

from app.auth.models import UserResponse
from app.stats.models import StatsResponse
from app.stats.transport.me import me_stats_endpoint


class TestMeStatsEndpoint(unittest.TestCase):
    @patch("app.stats.transport.me.get_user_stats", autospec=True)
    def test_delegates_to_service_with_current_user_id(self, mock_get_user_stats):
        mock_session = MagicMock()
        current_user = UserResponse(id="u1", email="u1@example.com", name="User One")
        expected_response = StatsResponse(
            total_rounds=3, total_attempts=7, average_score=26.7, best_score=50.0, recent_attempts=[],
        )
        mock_get_user_stats.return_value = expected_response

        response = me_stats_endpoint(current_user=current_user, session=mock_session)

        self.assertEqual(response.data, expected_response)
        mock_get_user_stats.assert_called_once_with(session=mock_session, user_id="u1")
