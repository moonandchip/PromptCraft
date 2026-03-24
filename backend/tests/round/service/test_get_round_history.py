import unittest
from unittest.mock import MagicMock, patch

from app.round.models import RoundHistoryResponse
from app.round.service.get_round_history import get_round_history


class TestGetRoundHistory(unittest.TestCase):
    @patch("app.round.service.get_round_history.get_round_history_by_user_id")
    def test_returns_empty_list_when_no_history(self, mock_data):
        mock_data.return_value = []
        session = MagicMock()

        result = get_round_history(session=session, user_id="u1")

        self.assertEqual(result, [])

    @patch("app.round.service.get_round_history.get_round_history_by_user_id")
    def test_enriches_with_round_info(self, mock_data):
        mock_data.return_value = [
            ("ancient-temple", 75.3, 3),
            ("futuristic-city", 42.1, 1),
        ]
        session = MagicMock()

        result = get_round_history(session=session, user_id="u1")

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], RoundHistoryResponse)
        self.assertEqual(result[0].round_id, "ancient-temple")
        self.assertEqual(result[0].title, "Ancient Temple")
        self.assertEqual(result[0].difficulty, "medium")
        self.assertEqual(result[0].target_image_url, "/static/ancient-temple.jpg")
        self.assertEqual(result[0].best_score, 75.3)
        self.assertEqual(result[0].attempt_count, 3)

        self.assertEqual(result[1].round_id, "futuristic-city")
        self.assertEqual(result[1].title, "Futuristic City")

    @patch("app.round.service.get_round_history.get_round_history_by_user_id")
    def test_skips_unknown_round_ids(self, mock_data):
        mock_data.return_value = [
            ("unknown-round", 50.0, 2),
            ("ancient-temple", 75.3, 3),
        ]
        session = MagicMock()

        result = get_round_history(session=session, user_id="u1")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].round_id, "ancient-temple")
