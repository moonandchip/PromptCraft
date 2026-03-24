import unittest

from app.stats.models import StatsResponse
from app.response import ApiResponse
from app.stats.transport.router import router


class TestStatsRouterModule(unittest.TestCase):
    def test_router_has_expected_stats_me_route(self):
        route_by_path = {route.path: route for route in router.routes}
        self.assertIn("/stats/me", route_by_path)
        route = route_by_path["/stats/me"]
        self.assertIn("GET", route.methods)
        self.assertEqual(route.response_model, ApiResponse[StatsResponse])
