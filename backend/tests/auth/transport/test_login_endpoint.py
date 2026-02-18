import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app.auth.models import LoginRequest, TokenResponse
from app.auth.service.errors import AuthServiceError
from app.auth.service.types import AuthServiceConfig
from app.auth.transport.login import login_endpoint


class TestLoginEndpointTransportFunction(unittest.TestCase):
    @patch("app.auth.transport.login.login")
    def test_login_endpoint_success(self, mock_login):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_login.return_value = TokenResponse(access_token="token-abc")
        payload = LoginRequest(email="user@example.com", password="strongpass123")
        result = login_endpoint(payload, auth_service=config)
        self.assertEqual(result.access_token, "token-abc")

    @patch("app.auth.transport.login.login")
    def test_login_endpoint_maps_error(self, mock_login):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_login.side_effect = AuthServiceError(401, "invalid credentials")
        payload = LoginRequest(email="user@example.com", password="strongpass123")
        with self.assertRaises(HTTPException) as exc:
            login_endpoint(payload, auth_service=config)
        self.assertEqual(exc.exception.status_code, 401)
