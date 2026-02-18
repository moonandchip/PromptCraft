import unittest
from unittest.mock import patch

from app.auth.models import RegisterRequest, UserResponse
from app.auth.service.auth_service import AuthService


class TestAuthServiceRegisterUserMethod(unittest.TestCase):
    @patch("app.auth.service.auth_service.register_user")
    def test_auth_service_register_user_method(self, mock_register_user):
        mock_register_user.return_value = UserResponse(id="u1", email="user@example.com", name="User")
        service = AuthService(base_url="http://auth.test")
        user = service.register_user(RegisterRequest(email="user@example.com", password="strongpass123", name="User"))
        self.assertEqual(user.id, "u1")
