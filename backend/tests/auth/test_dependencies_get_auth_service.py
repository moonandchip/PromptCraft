import unittest

from app.auth.dependencies import get_auth_service as dependencies_get_auth_service
from app.auth.transport.get_auth_service import get_auth_service as transport_get_auth_service


class TestDependenciesGetAuthService(unittest.TestCase):
    def test_dependencies_get_auth_service_aliases_transport_function(self):
        self.assertIs(dependencies_get_auth_service, transport_get_auth_service)
