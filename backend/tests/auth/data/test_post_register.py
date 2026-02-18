import unittest
from unittest.mock import patch

from app.auth.data.post_register import post_register


class TestPostRegister(unittest.TestCase):
    @patch("app.auth.data.post_register.request_auth_service")
    def test_post_register_calls_request_auth_service(self, mock_request_auth_service):
        mock_request_auth_service.return_value = {"user": {"id": "u1", "email": "user@example.com"}}
        result = post_register(
            email="user@example.com",
            password="strongpass123",
            name="User",
            base_url="http://auth.test",
            timeout_seconds=10.0,
        )
        self.assertIn("user", result)
        mock_request_auth_service.assert_called_once()
