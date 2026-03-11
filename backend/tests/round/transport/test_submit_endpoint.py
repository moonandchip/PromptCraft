"""Tests for round transport endpoint functions."""

import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from app.auth.models import UserResponse
from app.round.models import RoundInfo, SubmitRequest, SubmitResponse
from app.round.service.errors import RoundServiceError
from app.round.transport.get_rounds_endpoint import get_rounds_endpoint
from app.round.transport.submit_endpoint import submit_endpoint

_MOCK_USER = UserResponse(id="user-uuid-1234", email="test@example.com")


class TestGetRoundsEndpoint(unittest.TestCase):
    @patch("app.round.transport.get_rounds_endpoint.get_rounds", autospec=True)
    def test_get_rounds_endpoint_delegates_to_service(self, mock_get_rounds):
        expected_rounds = [
            RoundInfo(
                id="golden-sunset",
                title="Golden Sunset",
                difficulty="easy",
                reference_image="golden-sunset.jpeg",
            )
        ]
        mock_get_rounds.return_value = expected_rounds

        result = get_rounds_endpoint()

        self.assertEqual(result, expected_rounds)
        mock_get_rounds.assert_called_once_with()


class TestSubmitEndpoint(unittest.TestCase):
    @patch("app.round.transport.submit_endpoint.submit_round", autospec=True)
    def test_submit_endpoint_returns_service_response(self, mock_submit_round):
        expected = SubmitResponse(generated_image_url="https://example.com/generated.jpg", similarity_score=72.5)
        mock_submit_round.return_value = expected
        session = MagicMock()
        body = SubmitRequest(round_id="ancient-temple", user_prompt="a majestic scene")

        response = submit_endpoint(body=body, current_user=_MOCK_USER, session=session)

        self.assertEqual(response, expected)
        mock_submit_round.assert_called_once_with(
            session=session,
            user_email="test@example.com",
            round_id="ancient-temple",
            user_prompt="a majestic scene",
        )

    @patch("app.round.transport.submit_endpoint.submit_round", autospec=True)
    def test_submit_endpoint_maps_round_service_error_to_http_exception(self, mock_submit_round):
        mock_submit_round.side_effect = RoundServiceError(status_code=404, detail="Round not found")
        session = MagicMock()
        body = SubmitRequest(round_id="missing-round", user_prompt="some prompt")

        with self.assertRaises(HTTPException) as ctx:
            submit_endpoint(body=body, current_user=_MOCK_USER, session=session)

        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.detail, "Round not found")
