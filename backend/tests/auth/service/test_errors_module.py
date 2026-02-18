import unittest

from app.auth.service.errors import AuthServiceError


class TestErrorsModule(unittest.TestCase):
    def test_auth_service_error_sets_fields(self):
        err = AuthServiceError(401, "invalid token")
        self.assertEqual(err.status_code, 401)
        self.assertEqual(err.detail, "invalid token")
