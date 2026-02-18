import unittest

from app.auth.transport.router import router


class TestTransportRouterModule(unittest.TestCase):
    def test_router_has_expected_routes(self):
        route_paths = {route.path for route in router.routes}
        self.assertIn("/auth/register", route_paths)
        self.assertIn("/auth/login", route_paths)
        self.assertIn("/auth/me", route_paths)
