import importlib
import unittest
from unittest.mock import MagicMock, patch

from app.round.exceptions import StartRoundException
from app.round.types.args import StartRoundArgs

start_round_module = importlib.import_module("app.round.service.start_round")
start_round = start_round_module.start_round
_select_round = start_round_module._select_round


def _round_dict(**overrides):
    base = {
        "id": "golden-sunset",
        "title": "Golden Sunset",
        "difficulty": "easy",
        "reference_image": "golden-sunset.jpeg",
        "target_prompt": "A glowing golden sunset over the ocean.",
    }
    base.update(overrides)
    return base


class TestStartRound(unittest.TestCase):
    @patch.object(start_round_module, "upsert_user_profile", autospec=True)
    @patch.object(start_round_module, "save_round_start", autospec=True)
    @patch.object(start_round_module, "choice", autospec=True)
    def test_start_round_returns_selected_round_payload(self, mock_choice, mock_save_round_start, mock_upsert_user_profile):
        mock_choice.return_value = _round_dict()
        mock_upsert_user_profile.return_value = "u1"
        session = MagicMock()

        response = start_round(session=session, args=StartRoundArgs(user_id="u1", user_email="user@example.com"))

        self.assertEqual(response.round_id, "golden-sunset")
        self.assertEqual(response.target_image_url, "/static/golden-sunset.jpeg")
        self.assertEqual(response.title, "Golden Sunset")
        self.assertEqual(response.difficulty, "easy")
        self.assertEqual(response.target_prompt, "A glowing golden sunset over the ocean.")
        mock_upsert_user_profile.assert_called_once_with(
            session,
            user_id="u1",
            email="user@example.com",
            display_name=None,
        )
        mock_save_round_start.assert_called_once_with(
            session=session,
            user_id="u1",
            round_id="golden-sunset",
            target_image_url="/static/golden-sunset.jpeg",
        )

    @patch.object(start_round_module, "upsert_user_profile", autospec=True)
    @patch.object(start_round_module, "save_round_start", autospec=True)
    @patch.object(start_round_module, "choice", autospec=True)
    def test_start_round_defaults_target_prompt_to_empty_string(self, mock_choice, mock_save_round_start, mock_upsert_user_profile):
        round_without_prompt = _round_dict()
        round_without_prompt.pop("target_prompt")
        mock_choice.return_value = round_without_prompt
        mock_upsert_user_profile.return_value = "u1"

        response = start_round(session=MagicMock(), args=StartRoundArgs(user_id="u1", user_email="user@example.com"))

        self.assertEqual(response.target_prompt, "")

    @patch.object(start_round_module, "upsert_user_profile", autospec=True)
    @patch.object(start_round_module, "save_round_start", autospec=True)
    @patch.object(start_round_module, "choice", autospec=True)
    def test_start_round_maps_persistence_failure(self, mock_choice, mock_save_round_start, mock_upsert_user_profile):
        mock_choice.return_value = _round_dict()
        mock_upsert_user_profile.return_value = "u1"
        mock_save_round_start.side_effect = Exception("DB down")
        session = MagicMock()

        with self.assertRaises(StartRoundException) as ctx:
            start_round(session=session, args=StartRoundArgs(user_id="u1", user_email="user@example.com"))

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertEqual(ctx.exception.message, "Failed to start round")


class TestSelectRound(unittest.TestCase):
    def setUp(self):
        self.rounds_patcher = patch.object(
            start_round_module,
            "ROUNDS",
            [
                {"id": "r-easy", "title": "E", "difficulty": "easy", "reference_image": "e.jpg"},
                {"id": "r-med", "title": "M", "difficulty": "medium", "reference_image": "m.jpg"},
                {"id": "r-hard", "title": "H", "difficulty": "hard", "reference_image": "h.jpg"},
            ],
        )
        self.rounds_patcher.start()
        self.addCleanup(self.rounds_patcher.stop)

    def test_select_round_filters_by_difficulty(self):
        for _ in range(20):
            selected = _select_round("hard")
            self.assertEqual(selected["difficulty"], "hard")

    def test_select_round_normalises_difficulty_case(self):
        for _ in range(20):
            selected = _select_round("EASY")
            self.assertEqual(selected["difficulty"], "easy")

    def test_select_round_returns_any_for_invalid_difficulty(self):
        selected = _select_round("ultra-extreme")
        self.assertIn(selected["difficulty"], {"easy", "medium", "hard"})

    def test_select_round_returns_any_when_no_difficulty_provided(self):
        selected = _select_round(None)
        self.assertIn(selected["difficulty"], {"easy", "medium", "hard"})

    def test_select_round_falls_back_when_difficulty_has_no_candidates(self):
        with patch.object(
            start_round_module,
            "ROUNDS",
            [{"id": "only", "title": "Only", "difficulty": "easy", "reference_image": "o.jpg"}],
        ):
            selected = _select_round("hard")
            self.assertEqual(selected["id"], "only")
