import unittest
from unittest.mock import MagicMock, patch

from app.round.data.get_round_history_by_user_id import get_round_history_by_user_id


class TestGetRoundHistoryByUserId(unittest.TestCase):
    @patch("app.round.data.get_round_history_by_user_id.Session", autospec=True)
    def test_returns_empty_list_when_no_attempts(self, _mock_session_cls):
        session = MagicMock()
        session.execute.return_value.all.return_value = []

        result = get_round_history_by_user_id(session=session, user_id="u1")

        self.assertEqual(result, [])
        session.execute.assert_called_once()

    @patch("app.round.data.get_round_history_by_user_id.Session", autospec=True)
    def test_returns_grouped_rounds(self, _mock_session_cls):
        session = MagicMock()
        row1 = MagicMock()
        row1.round_id = "ancient-temple"
        row1.best_score = 75.3
        row1.attempt_count = 3

        row2 = MagicMock()
        row2.round_id = "futuristic-city"
        row2.best_score = 42.1
        row2.attempt_count = 1

        session.execute.return_value.all.return_value = [row1, row2]

        result = get_round_history_by_user_id(session=session, user_id="u1")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("ancient-temple", 75.3, 3))
        self.assertEqual(result[1], ("futuristic-city", 42.1, 1))

    @patch("app.round.data.get_round_history_by_user_id.Session", autospec=True)
    def test_handles_null_best_score(self, _mock_session_cls):
        session = MagicMock()
        row = MagicMock()
        row.round_id = "golden-sunset"
        row.best_score = None
        row.attempt_count = 1
        session.execute.return_value.all.return_value = [row]

        result = get_round_history_by_user_id(session=session, user_id="u1")

        self.assertEqual(result[0], ("golden-sunset", 0.0, 1))
