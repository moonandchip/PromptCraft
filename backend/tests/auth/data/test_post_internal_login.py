import unittest
from unittest.mock import patch

from app.auth.data.post_internal_login import post_internal_login


class TestPostInternalLogin(unittest.TestCase):
    @patch("app.auth.data.post_internal_login.request_auth_service")
    def test_post_internal_login_calls_request_auth_service(self, mock_request_auth_service):
        mock_request_auth_service.return_value = {"access_token": "abc"}
        result = post_internal_login(
            email="user@example.com",
            password="strongpass123",
            base_url="http://auth.test",
            timeout_seconds=10.0,
        )
        self.assertEqual(result["access_token"], "abc")
        mock_request_auth_service.assert_called_once()
