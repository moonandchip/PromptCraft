import importlib
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from app.challenge.exceptions import GetCurrentChallengeException
from app.challenge.types.args import GetCurrentChallengeArgs

module = importlib.import_module("app.challenge.service.get_current_challenge_view")


def _make_challenge(round_id="fixed-round", max_attempts=3):
    challenge = MagicMock()
    challenge.id = "c-1"
    challenge.period_type = "daily"
    challenge.period_end = datetime(2026, 4, 21, tzinfo=timezone.utc)
    challenge.round_id = round_id
    challenge.max_attempts = max_attempts
    return challenge


class TestGetCurrentChallengeView(unittest.TestCase):
    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_returns_state_with_progress(self, mock_get_or_create, mock_get_round, mock_get_progress):
        mock_get_or_create.return_value = _make_challenge()
        mock_get_round.return_value = {
            "id": "fixed-round",
            "title": "Fixed Round",
            "difficulty": "medium",
            "reference_image": "fixed.jpg",
        }
        mock_get_progress.return_value = (1, 42.5)

        result = module.get_current_challenge_view(session=MagicMock(), args=GetCurrentChallengeArgs(user_id="u1"))

        self.assertEqual(result.challenge_id, "c-1")
        self.assertEqual(result.round_id, "fixed-round")
        self.assertEqual(result.title, "Fixed Round")
        self.assertEqual(result.difficulty, "medium")
        self.assertEqual(result.target_image_url, "/static/fixed.jpg")
        self.assertEqual(result.attempts_used, 1)
        self.assertEqual(result.best_score, 42.5)
        self.assertEqual(result.max_attempts, 3)

    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_raises_not_found_when_round_unknown(self, mock_get_or_create, mock_get_round):
        mock_get_or_create.return_value = _make_challenge(round_id="missing")
        mock_get_round.return_value = None

        with patch.dict(module._ROUNDS_BY_ID, {}, clear=True):
            with self.assertRaises(GetCurrentChallengeException) as ctx:
                module.get_current_challenge_view(session=MagicMock(), args=GetCurrentChallengeArgs(user_id="u1"))

        self.assertEqual(ctx.exception.status_code, 404)

    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_falls_back_to_module_round_lookup(self, mock_get_or_create, mock_get_round, mock_get_progress):
        mock_get_or_create.return_value = _make_challenge(round_id="from-module")
        mock_get_round.return_value = None
        mock_get_progress.return_value = (0, 0.0)

        with patch.dict(
            module._ROUNDS_BY_ID,
            {"from-module": {"id": "from-module", "title": "X", "difficulty": "easy", "reference_image": "x.jpg"}},
            clear=True,
        ):
            result = module.get_current_challenge_view(session=MagicMock(), args=GetCurrentChallengeArgs(user_id="u1"))

        self.assertEqual(result.title, "X")
