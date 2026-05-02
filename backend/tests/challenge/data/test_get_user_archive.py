import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.challenge.data.get_user_archive import get_user_archive


def _challenge(challenge_id, day):
    period_start = datetime(2026, 4, day, tzinfo=timezone.utc)
    period_end = datetime(2026, 4, day + 1, tzinfo=timezone.utc)
    return SimpleNamespace(
        id=challenge_id,
        period_start=period_start,
        period_end=period_end,
        round_id="ancient-temple",
        max_attempts=3,
    )


class TestGetUserArchive(unittest.TestCase):
    def test_returns_empty_when_no_challenges(self):
        session = MagicMock()
        session.execute.return_value.scalars.return_value = iter([])

        self.assertEqual(get_user_archive(session=session, user_id="u1"), [])

    def test_joins_progress_into_each_challenge(self):
        challenges = [_challenge("c-2", 21), _challenge("c-1", 20)]
        progress_rows = [
            SimpleNamespace(challenge_id="c-1", attempts_used=3, best_score=80.0),
            SimpleNamespace(challenge_id="c-2", attempts_used=1, best_score=42.5),
        ]

        session = MagicMock()
        call_count = [0]

        def execute_side_effect(_query):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] == 1:
                result.scalars.return_value = iter(challenges)
            else:
                result.all.return_value = progress_rows
            return result

        session.execute.side_effect = execute_side_effect

        archive = get_user_archive(session=session, user_id="u1")

        self.assertEqual(len(archive), 2)
        first, second = archive
        self.assertEqual(first["challenge_id"], "c-2")
        self.assertEqual(first["attempts_used"], 1)
        self.assertEqual(first["best_score"], 42.5)
        self.assertEqual(second["challenge_id"], "c-1")
        self.assertEqual(second["attempts_used"], 3)
        self.assertEqual(second["best_score"], 80.0)

    def test_unplayed_challenges_get_zero_progress(self):
        challenges = [_challenge("c-1", 20)]

        session = MagicMock()
        call_count = [0]

        def execute_side_effect(_query):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] == 1:
                result.scalars.return_value = iter(challenges)
            else:
                result.all.return_value = []
            return result

        session.execute.side_effect = execute_side_effect

        archive = get_user_archive(session=session, user_id="u1")

        self.assertEqual(archive[0]["attempts_used"], 0)
        self.assertEqual(archive[0]["best_score"], 0.0)
