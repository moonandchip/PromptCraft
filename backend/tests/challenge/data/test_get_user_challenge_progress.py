import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.challenge.data.get_user_challenge_progress import get_user_challenge_progress


class TestGetUserChallengeProgress(unittest.TestCase):
    def test_returns_attempts_used_and_best_score(self):
        session = MagicMock()
        session.execute.return_value.one.return_value = SimpleNamespace(
            attempts_used=2, best_score=88.5,
        )

        attempts_used, best_score = get_user_challenge_progress(
            session=session, user_id="u1", challenge_id="c-1",
        )

        self.assertEqual(attempts_used, 2)
        self.assertEqual(best_score, 88.5)

    def test_coerces_none_aggregates_to_zero(self):
        session = MagicMock()
        session.execute.return_value.one.return_value = SimpleNamespace(
            attempts_used=None, best_score=None,
        )

        attempts_used, best_score = get_user_challenge_progress(
            session=session, user_id="u1", challenge_id="c-1",
        )

        self.assertEqual(attempts_used, 0)
        self.assertEqual(best_score, 0.0)

    def test_returns_int_and_float_types(self):
        session = MagicMock()
        session.execute.return_value.one.return_value = SimpleNamespace(
            attempts_used="3", best_score="55",
        )

        attempts_used, best_score = get_user_challenge_progress(
            session=session, user_id="u1", challenge_id="c-1",
        )

        self.assertIsInstance(attempts_used, int)
        self.assertIsInstance(best_score, float)
