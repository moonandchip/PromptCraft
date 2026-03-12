import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from app.auth.models import UserResponse
from app.round.models import StartRoundResponse
from app.round.service.errors import RoundServiceError
from app.round.transport.start_endpoint import start_endpoint


class TestStartEndpoint(unittest.TestCase):
    @patch("app.round.transport.start_endpoint.start_round", autospec=True)
    def test_start_endpoint_returns_service_response(self, mock_start_round):
        expected = StartRoundResponse(
            round_id="ancient-temple",
            target_image_url="/static/ancient-temple.jpg",
        )
        mock_start_round.return_value = expected
        current_user = UserResponse(id="u1", email="user@example.com", name="User")
        session = MagicMock()

        response = start_endpoint(current_user=current_user, session=session)

        self.assertEqual(response, expected)
        mock_start_round.assert_called_once_with(session=session, user_id="u1")

    @patch("app.round.transport.start_endpoint.start_round", autospec=True)
    def test_start_endpoint_maps_service_error_to_http_exception(self, mock_start_round):
        mock_start_round.side_effect = RoundServiceError(status_code=500, detail="Failed to start round")
        current_user = UserResponse(id="u1", email="user@example.com", name="User")
        session = MagicMock()

        with self.assertRaises(HTTPException) as ctx:
            start_endpoint(current_user=current_user, session=session)

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertEqual(ctx.exception.detail, "Failed to start round")
