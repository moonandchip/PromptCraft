import unittest

from app.challenge import constants


class TestChallengeConstants(unittest.TestCase):
    def test_router_prefix(self):
        self.assertEqual(constants.ROUTER_PREFIX, "/challenge")

    def test_router_tag(self):
        self.assertEqual(constants.ROUTER_TAG, "challenge")

    def test_period_daily_value(self):
        self.assertEqual(constants.PERIOD_DAILY, "daily")

    def test_default_max_attempts_is_positive(self):
        self.assertGreater(constants.DEFAULT_MAX_ATTEMPTS, 0)

    def test_leaderboard_limit_is_positive(self):
        self.assertGreater(constants.LEADERBOARD_LIMIT, 0)

    def test_channel_namespace(self):
        self.assertTrue(constants.CHANNEL.startswith("promptcraft."))

    def test_feature_constants_are_strings(self):
        for value in (
            constants.GET_CURRENT_FEATURE,
            constants.SUBMIT_CHALLENGE_FEATURE,
            constants.GET_LEADERBOARD_FEATURE,
        ):
            self.assertIsInstance(value, str)
            self.assertTrue(value)
