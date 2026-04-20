import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from app.challenge.data.get_active_challenge import get_active_challenge


class TestGetActiveChallenge(unittest.TestCase):
    def test_returns_value_from_session_execute(self):
        session = MagicMock()
        sentinel_challenge = object()
        session.execute.return_value.scalar_one_or_none.return_value = sentinel_challenge

        result = get_active_challenge(session=session, period_type="daily", now=datetime.now(timezone.utc))

        self.assertIs(result, sentinel_challenge)
        session.execute.assert_called_once()

    def test_returns_none_when_no_active_challenge(self):
        session = MagicMock()
        session.execute.return_value.scalar_one_or_none.return_value = None

        result = get_active_challenge(session=session, period_type="daily", now=datetime.now(timezone.utc))

        self.assertIsNone(result)
