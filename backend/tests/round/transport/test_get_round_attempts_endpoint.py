import unittest
from unittest.mock import MagicMock, patch

from app.auth.models import UserResponse
from app.round.models import RoundAttemptResponse
from app.response import ApiResponse
from app.round.transport.get_round_attempts_endpoint import get_round_attempts_endpoint


class TestGetRoundAttemptsEndpoint(unittest.TestCase):
    @patch("app.round.transport.get_round_attempts_endpoint.get_round_attempts", autospec=True)
    def test_delegates_to_service_with_current_user_and_round_id(self, mock_get_round_attempts):
        expected = [
            RoundAttemptResponse(
                attempt_number=1,
                prompt="first prompt",
                generated_image_url="https://example.com/first.png",
                similarity_score=61.0,
            )
        ]
        mock_get_round_attempts.return_value = expected
        session = MagicMock()
        current_user = UserResponse(id="u1", email="u1@example.com", name="User One")

        response = get_round_attempts_endpoint(
            id="ancient-temple",
            current_user=current_user,
            session=session,
        )

        self.assertIsInstance(response, ApiResponse)
        self.assertEqual(response.data, expected)
        mock_get_round_attempts.assert_called_once_with(
            session=session,
            user_id="u1",
            round_id="ancient-temple",
        )
