import unittest
from unittest.mock import patch

from app.auth.domain.exceptions import AuthError, RegisterException
from app.auth.models import RegisterRequest, UserResponse
from app.auth.service.errors import AuthServiceError
from app.auth.service.types import AuthServiceConfig
from app.auth.transport.register import register_endpoint
from app.response import ApiResponse


class TestRegisterTransportFunction(unittest.TestCase):
    @patch("app.auth.transport.register.register_user")
    def test_register_success(self, mock_register_user):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_register_user.return_value = UserResponse(id="u1", email="user@example.com", name="User")
        payload = RegisterRequest(email="user@example.com", password="strongpass123", name="User")
        result = register_endpoint(payload, auth_service=config)
        self.assertIsInstance(result, ApiResponse)
        self.assertEqual(result.data.id, "u1")

    @patch("app.auth.transport.register.register_user")
    def test_register_maps_error(self, mock_register_user):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_register_user.side_effect = RegisterException(
            status_code=409, error_code=AuthError.INVALID_CREDENTIALS, message="email exists",
        )
        payload = RegisterRequest(email="user@example.com", password="strongpass123", name="User")
        with self.assertRaises(RegisterException) as exc:
            register_endpoint(payload, auth_service=config)
        self.assertEqual(exc.exception.status_code, 409)
