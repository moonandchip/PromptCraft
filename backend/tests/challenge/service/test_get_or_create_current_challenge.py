import importlib
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

module = importlib.import_module("app.challenge.service.get_or_create_current_challenge")


_FIXED_NOW = datetime(2026, 4, 20, 14, 30, tzinfo=timezone.utc)


class _FixedDatetime(datetime):
    @classmethod
    def now(cls, tz=None):  # noqa: D401 - matches datetime API
        return _FIXED_NOW


class TestUtcDayBounds(unittest.TestCase):
    def test_bounds_span_a_full_day(self):
        start, end = module._utc_day_bounds(_FIXED_NOW)
        self.assertEqual(start, datetime(2026, 4, 20, tzinfo=timezone.utc))
        self.assertEqual(end - start, timedelta(days=1))


class TestSelectRoundIdForDate(unittest.TestCase):
    def test_select_uses_modulo_of_ordinal(self):
        with patch.object(module, "ROUNDS", [{"id": "r1"}, {"id": "r2"}, {"id": "r3"}]):
            day = datetime(2026, 4, 20, tzinfo=timezone.utc)
            expected = [{"id": "r1"}, {"id": "r2"}, {"id": "r3"}][day.toordinal() % 3]["id"]
            self.assertEqual(module._select_round_id_for_date(day), expected)

    def test_select_rotates_across_consecutive_days(self):
        with patch.object(module, "ROUNDS", [{"id": "r1"}, {"id": "r2"}]):
            day1 = datetime(2026, 4, 20, tzinfo=timezone.utc)
            day2 = day1 + timedelta(days=1)
            self.assertNotEqual(
                module._select_round_id_for_date(day1),
                module._select_round_id_for_date(day2),
            )

    def test_select_raises_when_no_rounds_configured(self):
        with patch.object(module, "ROUNDS", []):
            with self.assertRaises(RuntimeError):
                module._select_round_id_for_date(_FIXED_NOW)


class TestGetOrCreateCurrentChallenge(unittest.TestCase):
    @patch.object(module, "create_challenge", autospec=True)
    @patch.object(module, "get_active_challenge", autospec=True)
    @patch.object(module, "datetime", _FixedDatetime)
    def test_returns_existing_challenge_without_creating(self, mock_get_active, mock_create):
        existing = object()
        mock_get_active.return_value = existing
        session = MagicMock()

        result = module.get_or_create_current_challenge(session=session)

        self.assertIs(result, existing)
        mock_create.assert_not_called()

    @patch.object(module, "create_challenge", autospec=True)
    @patch.object(module, "get_active_challenge", autospec=True)
    @patch.object(module, "datetime", _FixedDatetime)
    def test_creates_challenge_when_none_active(self, mock_get_active, mock_create):
        mock_get_active.return_value = None
        created = object()
        mock_create.return_value = created
        session = MagicMock()

        with patch.object(module, "ROUNDS", [{"id": "fixed-round"}]):
            result = module.get_or_create_current_challenge(session=session)

        self.assertIs(result, created)
        mock_create.assert_called_once()
        kwargs = mock_create.call_args.kwargs
        self.assertEqual(kwargs["period_type"], "daily")
        self.assertEqual(kwargs["round_id"], "fixed-round")
        self.assertEqual(kwargs["max_attempts"], 3)
        self.assertEqual(kwargs["period_start"], datetime(2026, 4, 20, tzinfo=timezone.utc))
        self.assertEqual(kwargs["period_end"], datetime(2026, 4, 21, tzinfo=timezone.utc))

    @patch.object(module, "get_active_challenge", autospec=True)
    @patch.object(module, "datetime", _FixedDatetime)
    def test_passes_now_to_lookup(self, mock_get_active):
        mock_get_active.return_value = MagicMock()
        module.get_or_create_current_challenge(session=MagicMock())

        kwargs = mock_get_active.call_args.kwargs
        self.assertEqual(kwargs["period_type"], "daily")
        self.assertEqual(kwargs["now"], _FIXED_NOW)
