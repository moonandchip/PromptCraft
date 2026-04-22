import unittest
from unittest.mock import MagicMock, patch

from app.auth.models import UserResponse
from app.challenge.exceptions import GetLeaderboardException
from app.challenge.models import LeaderboardResponse
from app.challenge.transport.leaderboard_endpoint import leaderboard_endpoint
from app.challenge.types.args import GetLeaderboardArgs
from app.response import ApiResponse


class TestLeaderboardEndpoint(unittest.TestCase):
    @patch("app.challenge.transport.leaderboard_endpoint.get_leaderboard_view", autospec=True)
    def test_returns_service_response(self, mock_view):
        expected = LeaderboardResponse(challenge_id="c-1", period_end="2026-04-21T00:00:00+00:00", entries=[])
        mock_view.return_value = expected
        current_user = UserResponse(id="u1", email="user@example.com", name="User")
        session = MagicMock()

        response = leaderboard_endpoint(limit=5, current_user=current_user, session=session)

        self.assertIsInstance(response, ApiResponse)
        self.assertEqual(response.data, expected)
        mock_view.assert_called_once_with(session=session, args=GetLeaderboardArgs(limit=5))

    @patch("app.challenge.transport.leaderboard_endpoint.get_leaderboard_view", autospec=True)
    def test_unexpected_error_wrapped_as_500(self, mock_view):
        mock_view.side_effect = RuntimeError("boom")

        with self.assertRaises(GetLeaderboardException) as ctx:
            leaderboard_endpoint(
                limit=10,
                current_user=UserResponse(id="u1", email="user@example.com", name="User"),
                session=MagicMock(),
            )

        self.assertEqual(ctx.exception.status_code, 500)
