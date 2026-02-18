import unittest

from app.auth.service.types import AuthServiceConfig


class TestTypesModule(unittest.TestCase):
    def test_auth_service_config_fields(self):
        config = AuthServiceConfig(base_url="http://auth.test", timeout_seconds=5.0)
        self.assertEqual(config.base_url, "http://auth.test")
        self.assertEqual(config.timeout_seconds, 5.0)
