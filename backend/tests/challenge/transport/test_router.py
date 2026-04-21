import unittest

from app.challenge.transport.router import router


class TestChallengeRouter(unittest.TestCase):
    def test_router_has_expected_routes(self):
        paths = {(route.path, tuple(sorted(route.methods))) for route in router.routes}
        self.assertIn(("/challenge/current", ("GET",)), paths)
        self.assertIn(("/challenge/submit", ("POST",)), paths)
        self.assertIn(("/challenge/leaderboard", ("GET",)), paths)

    def test_router_uses_challenge_tag(self):
        for route in router.routes:
            self.assertIn("challenge", route.tags)
