import unittest
from unittest.mock import patch

from app.auth.models import LoginRequest
from app.auth.service.errors import AuthServiceError
from app.auth.service.login import login
from app.auth.service.types import AuthServiceConfig


class TestLoginServiceFunction(unittest.TestCase):
    @patch("app.auth.service.login.post_internal_login")
    def test_login_success(self, mock_post_internal_login):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_post_internal_login.return_value = {"access_token": "token-abc", "token_type": "bearer"}
        token = login(LoginRequest(email="user@example.com", password="strongpass123"), config)
        self.assertEqual(token.access_token, "token-abc")

    @patch("app.auth.service.login.post_internal_login")
    def test_login_invalid_payload(self, mock_post_internal_login):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_post_internal_login.return_value = {"token_type": "bearer"}
        with self.assertRaises(AuthServiceError):
            login(LoginRequest(email="user@example.com", password="strongpass123"), config)
