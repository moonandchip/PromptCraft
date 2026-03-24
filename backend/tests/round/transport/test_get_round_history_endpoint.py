import unittest
from unittest.mock import MagicMock, patch

from app.auth.models import UserResponse
from app.response import ApiResponse
from app.round.models import RoundHistoryResponse
from app.round.transport.get_round_history_endpoint import get_round_history_endpoint


class TestGetRoundHistoryEndpoint(unittest.TestCase):
    @patch("app.round.transport.get_round_history_endpoint.get_round_history")
    def test_returns_api_response_with_history(self, mock_service):
        expected = [
            RoundHistoryResponse(
                round_id="ancient-temple",
                title="Ancient Temple",
                difficulty="medium",
                target_image_url="/static/ancient-temple.jpg",
                best_score=75.3,
                attempt_count=3,
            ),
        ]
        mock_service.return_value = expected
        session = MagicMock()
        current_user = UserResponse(id="u1", email="u1@example.com", name="User One")

        result = get_round_history_endpoint(current_user=current_user, session=session)

        self.assertIsInstance(result, ApiResponse)
        self.assertEqual(result.data, expected)
        mock_service.assert_called_once_with(session=session, user_id="u1")

    @patch("app.round.transport.get_round_history_endpoint.get_round_history")
    def test_returns_empty_list_when_no_history(self, mock_service):
        mock_service.return_value = []
        session = MagicMock()
        current_user = UserResponse(id="u1", email="u1@example.com", name="User One")

        result = get_round_history_endpoint(current_user=current_user, session=session)

        self.assertEqual(result.data, [])
