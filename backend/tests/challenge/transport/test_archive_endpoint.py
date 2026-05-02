import unittest
from unittest.mock import MagicMock, patch

from app.auth.models import UserResponse
from app.challenge.exceptions import ChallengeError, GetArchiveException
from app.challenge.models import ArchiveResponse
from app.challenge.transport.archive_endpoint import archive_endpoint
from app.response import ApiResponse


class TestArchiveEndpoint(unittest.TestCase):
    @patch("app.challenge.transport.archive_endpoint.get_archive_view", autospec=True)
    def test_returns_archive_response(self, mock_get_archive_view):
        expected = ArchiveResponse(entries=[])
        mock_get_archive_view.return_value = expected
        current_user = UserResponse(id="u1", email="u1@example.com", name="User")
        session = MagicMock()

        response = archive_endpoint(limit=30, current_user=current_user, session=session)

        self.assertIsInstance(response, ApiResponse)
        self.assertEqual(response.data, expected)
        kwargs = mock_get_archive_view.call_args.kwargs
        self.assertEqual(kwargs["session"], session)
        self.assertEqual(kwargs["args"].user_id, "u1")
        self.assertEqual(kwargs["args"].limit, 30)

    @patch("app.challenge.transport.archive_endpoint.get_archive_view", autospec=True)
    def test_wraps_unexpected_error_in_archive_exception(self, mock_get_archive_view):
        mock_get_archive_view.side_effect = RuntimeError("kaboom")
        current_user = UserResponse(id="u1", email="u1@example.com", name="User")

        with self.assertRaises(GetArchiveException) as ctx:
            archive_endpoint(limit=30, current_user=current_user, session=MagicMock())

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertEqual(ctx.exception.error, ChallengeError.UNKNOWN_ERROR)
