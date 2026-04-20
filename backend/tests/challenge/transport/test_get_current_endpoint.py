import unittest
from unittest.mock import MagicMock, patch

from app.auth.models import UserResponse
from app.challenge.exceptions import ChallengeError, GetCurrentChallengeException
from app.challenge.models import ChallengeStateResponse
from app.challenge.transport.get_current_endpoint import get_current_endpoint
from app.challenge.types.args import GetCurrentChallengeArgs
from app.response import ApiResponse


def _state(**overrides):
    base = {
        "challenge_id": "c-1",
        "period_type": "daily",
        "period_end": "2026-04-21T00:00:00+00:00",
        "round_id": "r1",
        "title": "Round One",
        "difficulty": "easy",
        "target_image_url": "/static/r1.jpg",
        "max_attempts": 3,
        "attempts_used": 0,
        "best_score": 0.0,
    }
    base.update(overrides)
    return ChallengeStateResponse(**base)


class TestGetCurrentEndpoint(unittest.TestCase):
    @patch("app.challenge.transport.get_current_endpoint.get_current_challenge_view", autospec=True)
    def test_returns_service_response(self, mock_view):
        expected = _state()
        mock_view.return_value = expected
        current_user = UserResponse(id="u1", email="user@example.com", name="User")
        session = MagicMock()

        response = get_current_endpoint(current_user=current_user, session=session)

        self.assertIsInstance(response, ApiResponse)
        self.assertEqual(response.data, expected)
        mock_view.assert_called_once_with(session=session, args=GetCurrentChallengeArgs(user_id="u1"))

    @patch("app.challenge.transport.get_current_endpoint.get_current_challenge_view", autospec=True)
    def test_passes_through_app_exception(self, mock_view):
        mock_view.side_effect = GetCurrentChallengeException(ChallengeError.NOT_FOUND, message="missing")

        with self.assertRaises(GetCurrentChallengeException) as ctx:
            get_current_endpoint(
                current_user=UserResponse(id="u1", email="user@example.com", name="User"),
                session=MagicMock(),
            )

        self.assertEqual(ctx.exception.status_code, 404)

    @patch("app.challenge.transport.get_current_endpoint.get_current_challenge_view", autospec=True)
    def test_wraps_unexpected_error(self, mock_view):
        mock_view.side_effect = RuntimeError("boom")

        with self.assertRaises(GetCurrentChallengeException) as ctx:
            get_current_endpoint(
                current_user=UserResponse(id="u1", email="user@example.com", name="User"),
                session=MagicMock(),
            )

        self.assertEqual(ctx.exception.status_code, 500)
