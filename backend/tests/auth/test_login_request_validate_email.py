import unittest

from app.auth.models import LoginRequest


class TestLoginRequestValidateEmail(unittest.TestCase):
    def test_login_request_normalizes_email(self):
        payload = LoginRequest(email="  USER@Example.com  ", password="strongpass123")
        self.assertEqual(payload.email, "user@example.com")
