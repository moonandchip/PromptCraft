import unittest
from unittest.mock import patch

from app.auth.models import LoginRequest, TokenResponse
from app.auth.service.auth_service import AuthService


class TestAuthServiceLoginMethod(unittest.TestCase):
    @patch("app.auth.service.auth_service.login")
    def test_auth_service_login_method(self, mock_login):
        mock_login.return_value = TokenResponse(access_token="token-abc")
        service = AuthService(base_url="http://auth.test")
        token = service.login(LoginRequest(email="user@example.com", password="strongpass123"))
        self.assertEqual(token.access_token, "token-abc")
