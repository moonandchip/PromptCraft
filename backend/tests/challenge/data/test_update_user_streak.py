import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock

from app.challenge.data.update_user_streak import update_user_streak
from app.round.data.entities import UserProfile


def _profile(current=0, longest=0, last_played=None):
    profile = MagicMock(spec=UserProfile)
    profile.current_streak = current
    profile.longest_streak = longest
    profile.last_played_date = last_played
    return profile


class TestUpdateUserStreak(unittest.TestCase):
    def test_first_ever_play_sets_streak_to_one(self):
        profile = _profile()
        session = MagicMock()
        session.get.return_value = profile
        today = date(2026, 4, 30)

        current, longest = update_user_streak(session=session, user_id="u1", today=today)

        self.assertEqual(current, 1)
        self.assertEqual(longest, 1)
        self.assertEqual(profile.last_played_date, today)
        session.flush.assert_called_once()

    def test_play_yesterday_increments_streak(self):
        today = date(2026, 4, 30)
        profile = _profile(current=4, longest=4, last_played=today - timedelta(days=1))
        session = MagicMock()
        session.get.return_value = profile

        current, longest = update_user_streak(session=session, user_id="u1", today=today)

        self.assertEqual(current, 5)
        self.assertEqual(longest, 5)
        self.assertEqual(profile.last_played_date, today)

    def test_play_today_is_idempotent(self):
        today = date(2026, 4, 30)
        profile = _profile(current=7, longest=10, last_played=today)
        session = MagicMock()
        session.get.return_value = profile

        current, longest = update_user_streak(session=session, user_id="u1", today=today)

        self.assertEqual(current, 7)
        self.assertEqual(longest, 10)
        # last_played_date unchanged
        self.assertEqual(profile.last_played_date, today)
        session.flush.assert_not_called()

    def test_gap_of_two_or_more_days_resets_streak(self):
        today = date(2026, 4, 30)
        profile = _profile(current=10, longest=10, last_played=today - timedelta(days=3))
        session = MagicMock()
        session.get.return_value = profile

        current, longest = update_user_streak(session=session, user_id="u1", today=today)

        self.assertEqual(current, 1)
        # longest preserved
        self.assertEqual(longest, 10)

    def test_increment_does_not_lower_longest_streak(self):
        today = date(2026, 4, 30)
        profile = _profile(current=2, longest=15, last_played=today - timedelta(days=1))
        session = MagicMock()
        session.get.return_value = profile

        current, longest = update_user_streak(session=session, user_id="u1", today=today)

        self.assertEqual(current, 3)
        self.assertEqual(longest, 15)

    def test_missing_profile_returns_zeros_without_raising(self):
        session = MagicMock()
        session.get.return_value = None

        current, longest = update_user_streak(session=session, user_id="u1", today=date(2026, 4, 30))

        self.assertEqual((current, longest), (0, 0))
        session.flush.assert_not_called()
