import unittest
from unittest.mock import MagicMock, patch

from app.auth.models import UserResponse
from app.challenge.exceptions import ChallengeError, SubmitChallengeException
from app.challenge.models import ChallengeSubmitRequest, ChallengeSubmitResponse
from app.challenge.transport.submit_endpoint import submit_endpoint
from app.challenge.types.args import SubmitChallengeArgs
from app.response import ApiResponse


def _response():
    return ChallengeSubmitResponse(
        generated_image_url="https://example.com/g.jpg",
        similarity_score=70.0,
        attempts_used=1,
        attempts_remaining=2,
        best_score=70.0,
    )


class TestSubmitEndpoint(unittest.TestCase):
    @patch("app.challenge.transport.submit_endpoint.submit_challenge", autospec=True)
    def test_returns_service_response(self, mock_submit):
        mock_submit.return_value = _response()
        current_user = UserResponse(id="u1", email="user@example.com", name="User")
        session = MagicMock()

        response = submit_endpoint(
            body=ChallengeSubmitRequest(user_prompt="a vivid scene"),
            current_user=current_user,
            session=session,
        )

        self.assertIsInstance(response, ApiResponse)
        self.assertEqual(response.data, _response())
        mock_submit.assert_called_once_with(
            session=session,
            args=SubmitChallengeArgs(
                user_id="u1",
                user_email="user@example.com",
                user_prompt="a vivid scene",
                user_display_name="User",
            ),
        )

    @patch("app.challenge.transport.submit_endpoint.submit_challenge", autospec=True)
    def test_attempt_limit_error_bubbles_with_429(self, mock_submit):
        mock_submit.side_effect = SubmitChallengeException(
            ChallengeError.ATTEMPT_LIMIT_REACHED, message="limit reached",
        )

        with self.assertRaises(SubmitChallengeException) as ctx:
            submit_endpoint(
                body=ChallengeSubmitRequest(user_prompt="prompt"),
                current_user=UserResponse(id="u1", email="user@example.com", name="User"),
                session=MagicMock(),
            )

        self.assertEqual(ctx.exception.status_code, 429)

    @patch("app.challenge.transport.submit_endpoint.submit_challenge", autospec=True)
    def test_unexpected_error_wrapped_as_unknown(self, mock_submit):
        mock_submit.side_effect = RuntimeError("kaboom")

        with self.assertRaises(SubmitChallengeException) as ctx:
            submit_endpoint(
                body=ChallengeSubmitRequest(user_prompt="prompt"),
                current_user=UserResponse(id="u1", email="user@example.com", name="User"),
                session=MagicMock(),
            )

        self.assertEqual(ctx.exception.status_code, 500)
