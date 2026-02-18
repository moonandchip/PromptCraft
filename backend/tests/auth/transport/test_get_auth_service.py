import unittest

from app.auth.service.types import AuthServiceConfig
from app.auth.transport.get_auth_service import get_auth_service


class TestGetAuthServiceTransportFunction(unittest.TestCase):
    def test_get_auth_service_returns_singleton_config(self):
        config_a = get_auth_service()
        config_b = get_auth_service()
        self.assertIs(config_a, config_b)
        self.assertIsInstance(config_a, AuthServiceConfig)
