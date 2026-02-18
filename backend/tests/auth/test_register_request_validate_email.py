import unittest

from pydantic import ValidationError

from app.auth.models import RegisterRequest


class TestRegisterRequestValidateEmail(unittest.TestCase):
    def test_register_request_normalizes_email(self):
        payload = RegisterRequest(email="  USER@Example.com  ", password="strongpass123", name="User")
        self.assertEqual(payload.email, "user@example.com")

    def test_register_request_rejects_invalid_email(self):
        with self.assertRaises(ValidationError):
            RegisterRequest(email="invalid-email", password="strongpass123", name="User")
