import os
import unittest
from unittest.mock import patch

from app.auth.service.build_auth_service_config import build_auth_service_config


class TestBuildAuthServiceConfig(unittest.TestCase):
    def test_build_auth_service_config_reads_env(self):
        with patch.dict(os.environ, {"AUTH_SERVICE_URL": "http://env-auth.test"}, clear=False):
            config = build_auth_service_config(timeout_seconds=7.5)
        self.assertEqual(config.base_url, "http://env-auth.test")
        self.assertEqual(config.timeout_seconds, 7.5)

    def test_build_auth_service_config_override(self):
        config = build_auth_service_config(base_url="http://override-auth.test", timeout_seconds=3.0)
        self.assertEqual(config.base_url, "http://override-auth.test")
        self.assertEqual(config.timeout_seconds, 3.0)
