import unittest

from app.auth import constants


class TestConstantsModule(unittest.TestCase):
    def test_expected_router_prefix_constant(self):
        self.assertEqual(constants.ROUTER_PREFIX, "/auth")
