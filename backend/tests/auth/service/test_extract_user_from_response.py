import unittest

from app.auth.service.errors import AuthServiceError
from app.auth.service.extract_user_from_response import extract_user_from_response


class TestExtractUserFromResponse(unittest.TestCase):
    def test_extract_user_from_response_success(self):
        user = extract_user_from_response(
            {"user": {"id": "u1", "email": "user@example.com", "name": "User"}},
            "invalid auth response",
        )
        self.assertEqual(user.id, "u1")
        self.assertEqual(user.email, "user@example.com")

    def test_extract_user_from_response_invalid_payload(self):
        with self.assertRaises(AuthServiceError):
            extract_user_from_response({"user": {"id": 123, "email": None}}, "invalid auth response")
