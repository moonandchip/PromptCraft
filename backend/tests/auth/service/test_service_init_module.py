import unittest

from app.auth.service import AuthService
from app.auth.service.auth_service import AuthService as AuthServiceImpl


class TestServiceInitModule(unittest.TestCase):
    def test_service_init_re_exports(self):
        self.assertIs(AuthService, AuthServiceImpl)
