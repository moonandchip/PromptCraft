import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app.auth.models import RegisterRequest, UserResponse
from app.auth.service.errors import AuthServiceError
from app.auth.service.types import AuthServiceConfig
from app.auth.transport.register import register


class TestRegisterTransportFunction(unittest.TestCase):
    @patch("app.auth.transport.register.register_user")
    def test_register_success(self, mock_register_user):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_register_user.return_value = UserResponse(id="u1", email="user@example.com", name="User")
        payload = RegisterRequest(email="user@example.com", password="strongpass123", name="User")
        result = register(payload, auth_service=config)
        self.assertEqual(result.id, "u1")

    @patch("app.auth.transport.register.register_user")
    def test_register_maps_error(self, mock_register_user):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=10.0)
        mock_register_user.side_effect = AuthServiceError(409, "email exists")
        payload = RegisterRequest(email="user@example.com", password="strongpass123", name="User")
        with self.assertRaises(HTTPException) as exc:
            register(payload, auth_service=config)
        self.assertEqual(exc.exception.status_code, 409)
