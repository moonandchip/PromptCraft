import importlib
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from app.challenge.types.args import GetArchiveArgs

module = importlib.import_module("app.challenge.service.get_archive_view")


def _archive_row(challenge_id="c-1", round_id="ancient-temple", attempts_used=2, best_score=70.0):
    return {
        "challenge_id": challenge_id,
        "period_start": datetime(2026, 4, 20, tzinfo=timezone.utc),
        "period_end": datetime(2026, 4, 21, tzinfo=timezone.utc),
        "round_id": round_id,
        "max_attempts": 3,
        "attempts_used": attempts_used,
        "best_score": best_score,
    }


class TestGetArchiveView(unittest.TestCase):
    @patch.object(module, "get_user_archive", autospec=True)
    def test_maps_data_layer_rows_into_archive_response(self, mock_get_user_archive):
        mock_get_user_archive.return_value = [_archive_row()]

        with patch.dict(
            module._ROUNDS_BY_ID,
            {"ancient-temple": {"id": "ancient-temple", "title": "Ancient Temple", "difficulty": "medium", "reference_image": "ancient-temple.jpg"}},
            clear=True,
        ):
            result = module.get_archive_view(session=MagicMock(), args=GetArchiveArgs(user_id="u1", limit=30))

        self.assertEqual(len(result.entries), 1)
        entry = result.entries[0]
        self.assertEqual(entry.challenge_id, "c-1")
        self.assertEqual(entry.title, "Ancient Temple")
        self.assertEqual(entry.difficulty, "medium")
        self.assertEqual(entry.target_image_url, "/static/ancient-temple.jpg")
        self.assertEqual(entry.attempts_used, 2)
        self.assertEqual(entry.best_score, 70.0)

    @patch.object(module, "get_user_archive", autospec=True)
    def test_skips_entries_with_unknown_round(self, mock_get_user_archive):
        mock_get_user_archive.return_value = [
            _archive_row(round_id="missing-round"),
            _archive_row(challenge_id="c-2"),
        ]

        with patch.dict(
            module._ROUNDS_BY_ID,
            {"ancient-temple": {"id": "ancient-temple", "title": "Ancient Temple", "difficulty": "medium", "reference_image": "ancient-temple.jpg"}},
            clear=True,
        ):
            result = module.get_archive_view(session=MagicMock(), args=GetArchiveArgs(user_id="u1", limit=30))

        self.assertEqual(len(result.entries), 1)
        self.assertEqual(result.entries[0].challenge_id, "c-2")

    @patch.object(module, "get_user_archive", autospec=True)
    def test_passes_limit_through(self, mock_get_user_archive):
        mock_get_user_archive.return_value = []

        module.get_archive_view(session=MagicMock(), args=GetArchiveArgs(user_id="u1", limit=7))

        kwargs = mock_get_user_archive.call_args.kwargs
        self.assertEqual(kwargs["limit"], 7)
        self.assertEqual(kwargs["user_id"], "u1")
