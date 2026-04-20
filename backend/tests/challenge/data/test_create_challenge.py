import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import create_autospec

from sqlalchemy.orm import Session

from app.challenge.data.create_challenge import create_challenge


class TestCreateChallenge(unittest.TestCase):
    def test_persists_row_and_returns_it(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        period_start = datetime(2026, 4, 20, tzinfo=timezone.utc)
        period_end = period_start + timedelta(days=1)

        result = create_challenge(
            session=session,
            period_type="daily",
            period_start=period_start,
            period_end=period_end,
            round_id="ancient-temple",
            max_attempts=3,
        )

        session.add.assert_called_once_with(result)
        session.commit.assert_called_once_with()
        session.refresh.assert_called_once_with(result)

    def test_attributes_match_inputs(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        period_start = datetime(2026, 4, 20, tzinfo=timezone.utc)
        period_end = period_start + timedelta(days=1)

        result = create_challenge(
            session=session,
            period_type="weekly",
            period_start=period_start,
            period_end=period_end,
            round_id="golden-sunset",
            max_attempts=5,
        )

        self.assertEqual(result.period_type, "weekly")
        self.assertEqual(result.period_start, period_start)
        self.assertEqual(result.period_end, period_end)
        self.assertEqual(result.round_id, "golden-sunset")
        self.assertEqual(result.max_attempts, 5)
