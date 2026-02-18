import unittest

from app.auth.dependencies import get_current_user as dependencies_get_current_user
from app.auth.transport.get_current_user import get_current_user as transport_get_current_user


class TestDependenciesGetCurrentUser(unittest.TestCase):
    def test_dependencies_get_current_user_aliases_transport_function(self):
        self.assertIs(dependencies_get_current_user, transport_get_current_user)
