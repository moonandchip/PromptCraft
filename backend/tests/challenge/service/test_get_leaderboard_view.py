import importlib
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from app.challenge.types.args import GetLeaderboardArgs

module = importlib.import_module("app.challenge.service.get_leaderboard_view")


def _challenge():
    challenge = MagicMock()
    challenge.id = "c-1"
    challenge.period_end = datetime(2026, 4, 21, tzinfo=timezone.utc)
    return challenge


class TestGetLeaderboardView(unittest.TestCase):
    @patch.object(module, "get_leaderboard", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_builds_response_with_ranked_entries(self, mock_get_or_create, mock_get_leaderboard):
        mock_get_or_create.return_value = _challenge()
        mock_get_leaderboard.return_value = [
            ("u1", "Alice", 90.0, 2),
            ("u2", "Bob", 80.0, 1),
        ]

        result = module.get_leaderboard_view(session=MagicMock(), args=GetLeaderboardArgs(limit=10))

        self.assertEqual(result.challenge_id, "c-1")
        self.assertEqual(len(result.entries), 2)
        self.assertEqual(result.entries[0].rank, 1)
        self.assertEqual(result.entries[0].user_id, "u1")
        self.assertEqual(result.entries[1].rank, 2)
        self.assertEqual(result.entries[1].user_id, "u2")

    @patch.object(module, "get_leaderboard", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_passes_limit_through(self, mock_get_or_create, mock_get_leaderboard):
        mock_get_or_create.return_value = _challenge()
        mock_get_leaderboard.return_value = []

        module.get_leaderboard_view(session=MagicMock(), args=GetLeaderboardArgs(limit=5))

        kwargs = mock_get_leaderboard.call_args.kwargs
        self.assertEqual(kwargs["limit"], 5)
        self.assertEqual(kwargs["challenge_id"], "c-1")

    @patch.object(module, "get_leaderboard", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_empty_leaderboard_returns_empty_entries(self, mock_get_or_create, mock_get_leaderboard):
        mock_get_or_create.return_value = _challenge()
        mock_get_leaderboard.return_value = []

        result = module.get_leaderboard_view(session=MagicMock(), args=GetLeaderboardArgs(limit=10))

        self.assertEqual(result.entries, [])
