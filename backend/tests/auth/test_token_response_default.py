import unittest

from app.auth.models import TokenResponse


class TestTokenResponseDefault(unittest.TestCase):
    def test_token_response_defaults_to_bearer(self):
        token = TokenResponse(access_token="abc123")
        self.assertEqual(token.token_type, "bearer")
