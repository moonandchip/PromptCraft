import unittest
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth.constants import ERR_MISSING_BEARER_TOKEN
from app.auth.models import UserResponse
from app.auth.service.errors import AuthServiceError
from app.auth.service.types import AuthServiceConfig
from app.auth.transport.get_current_user import get_current_user


class TestGetCurrentUserTransportFunction(unittest.TestCase):
    def test_get_current_user_requires_bearer(self):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        with self.assertRaises(HTTPException) as exc:
            get_current_user(credentials=None, auth_service=config)
        self.assertEqual(exc.exception.status_code, 401)
        self.assertEqual(exc.exception.detail, ERR_MISSING_BEARER_TOKEN)

    @patch("app.auth.transport.get_current_user.resolve_user_from_token")
    def test_get_current_user_success(self, mock_resolve_user_from_token):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_resolve_user_from_token.return_value = UserResponse(id="u1", email="user@example.com", name="User")
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="token-abc")
        user = get_current_user(credentials=credentials, auth_service=config)
        self.assertEqual(user.id, "u1")

    @patch("app.auth.transport.get_current_user.resolve_user_from_token")
    def test_get_current_user_maps_error(self, mock_resolve_user_from_token):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_resolve_user_from_token.side_effect = AuthServiceError(401, "invalid token")
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="bad-token")
        with self.assertRaises(HTTPException) as exc:
            get_current_user(credentials=credentials, auth_service=config)
        self.assertEqual(exc.exception.status_code, 401)
        self.assertEqual(exc.exception.detail, "invalid token")
