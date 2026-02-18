import unittest
from unittest.mock import patch

from app.auth.models import UserResponse
from app.auth.service.auth_service import AuthService


class TestAuthServiceResolveUserFromTokenMethod(unittest.TestCase):
    @patch("app.auth.service.auth_service.resolve_user_from_token")
    def test_auth_service_resolve_user_from_token_method(self, mock_resolve_user_from_token):
        mock_resolve_user_from_token.return_value = UserResponse(id="u1", email="user@example.com", name="User")
        service = AuthService(base_url="http://auth.test")
        user = service.resolve_user_from_token("token-abc")
        self.assertEqual(user.id, "u1")
