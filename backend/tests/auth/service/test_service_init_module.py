import unittest

from app.auth.service import AuthService, AuthServiceError
from app.auth.service.auth_service import AuthService as AuthServiceImpl
from app.auth.service.errors import AuthServiceError as AuthServiceErrorImpl


class TestServiceInitModule(unittest.TestCase):
    def test_service_init_re_exports(self):
        self.assertIs(AuthService, AuthServiceImpl)
        self.assertIs(AuthServiceError, AuthServiceErrorImpl)
