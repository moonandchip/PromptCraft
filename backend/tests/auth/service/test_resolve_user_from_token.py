import unittest
from unittest.mock import patch

from app.auth.service.resolve_user_from_token import resolve_user_from_token
from app.auth.service.types import AuthServiceConfig


class TestResolveUserFromTokenServiceFunction(unittest.TestCase):
    @patch("app.auth.service.resolve_user_from_token.get_internal_me")
    def test_resolve_user_from_token_success(self, mock_get_internal_me):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_get_internal_me.return_value = {"user": {"id": "u1", "email": "user@example.com", "name": "User"}}
        user = resolve_user_from_token("token-abc", config)
        self.assertEqual(user.id, "u1")
        self.assertEqual(user.email, "user@example.com")
