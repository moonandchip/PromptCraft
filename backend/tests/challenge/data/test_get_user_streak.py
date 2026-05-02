import unittest
from unittest.mock import MagicMock

from app.challenge.data.get_user_streak import get_user_streak
from app.round.data.entities import UserProfile


class TestGetUserStreak(unittest.TestCase):
    def test_returns_streak_from_profile(self):
        profile = MagicMock(spec=UserProfile)
        profile.current_streak = 4
        profile.longest_streak = 12
        session = MagicMock()
        session.get.return_value = profile

        self.assertEqual(get_user_streak(session=session, user_id="u1"), (4, 12))
        session.get.assert_called_once_with(UserProfile, "u1")

    def test_returns_zeros_when_profile_missing(self):
        session = MagicMock()
        session.get.return_value = None

        self.assertEqual(get_user_streak(session=session, user_id="u1"), (0, 0))

    def test_handles_null_streak_columns(self):
        profile = MagicMock(spec=UserProfile)
        profile.current_streak = None
        profile.longest_streak = None
        session = MagicMock()
        session.get.return_value = profile

        self.assertEqual(get_user_streak(session=session, user_id="u1"), (0, 0))
