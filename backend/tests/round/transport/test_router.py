import unittest

from app.round.transport.router import router


class TestRoundTransportRouterModule(unittest.TestCase):
    def test_router_has_rounds_route(self):
        route_paths = {route.path for route in router.routes}
        self.assertIn("/round/rounds", route_paths)

    def test_router_has_submit_route(self):
        route_paths = {route.path for route in router.routes}
        self.assertIn("/round/submit", route_paths)

    def test_rounds_route_is_get(self):
        for route in router.routes:
            if route.path == "/round/rounds":
                self.assertIn("GET", route.methods)
                break

    def test_submit_route_is_post(self):
        for route in router.routes:
            if route.path == "/round/submit":
                self.assertIn("POST", route.methods)
                break
