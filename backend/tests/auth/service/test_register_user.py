import unittest
from unittest.mock import patch

from app.auth.models import RegisterRequest
from app.auth.service.register_user import register_user
from app.auth.service.types import AuthServiceConfig


class TestRegisterUserServiceFunction(unittest.TestCase):
    @patch("app.auth.service.register_user.post_register")
    def test_register_user_success(self, mock_post_register):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_post_register.return_value = {"user": {"id": "u1", "email": "user@example.com", "name": "User"}}
        user = register_user(
            RegisterRequest(email="user@example.com", password="strongpass123", name="User"),
            config,
        )
        self.assertEqual(user.id, "u1")
        self.assertEqual(user.email, "user@example.com")
