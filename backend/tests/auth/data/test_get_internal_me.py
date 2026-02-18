import unittest
from unittest.mock import patch

from app.auth.data.get_internal_me import get_internal_me


class TestGetInternalMe(unittest.TestCase):
    @patch("app.auth.data.get_internal_me.request_auth_service")
    def test_get_internal_me_calls_request_auth_service(self, mock_request_auth_service):
        mock_request_auth_service.return_value = {"user": {"id": "u1", "email": "user@example.com"}}
        result = get_internal_me(token="token-abc", base_url="http://auth.test", timeout_seconds=10.0)
        self.assertIn("user", result)
        mock_request_auth_service.assert_called_once()
