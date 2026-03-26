import unittest
from unittest.mock import MagicMock, patch

from app.round.exceptions import RoundError, StartRoundException
from app.round.service.start_round import start_round
from app.round.types.args import StartRoundArgs


class TestStartRound(unittest.TestCase):
    @patch("app.round.service.start_round.save_round_start", autospec=True)
    @patch("app.round.service.start_round.choice", autospec=True)
    def test_start_round_returns_selected_round_payload(self, mock_choice, mock_save_round_start):
        mock_choice.return_value = {
            "id": "golden-sunset",
            "reference_image": "golden-sunset.jpeg",
        }
        session = MagicMock()

        response = start_round(session=session, args=StartRoundArgs(user_id="u1"))

        self.assertEqual(response.round_id, "golden-sunset")
        self.assertEqual(response.target_image_url, "/static/golden-sunset.jpeg")
        mock_save_round_start.assert_called_once_with(
            session=session,
            user_id="u1",
            round_id="golden-sunset",
            target_image_url="/static/golden-sunset.jpeg",
        )

    @patch("app.round.service.start_round.save_round_start", autospec=True)
    @patch("app.round.service.start_round.choice", autospec=True)
    def test_start_round_maps_persistence_failure(self, mock_choice, mock_save_round_start):
        mock_choice.return_value = {
            "id": "golden-sunset",
            "reference_image": "golden-sunset.jpeg",
        }
        mock_save_round_start.side_effect = Exception("DB down")
        session = MagicMock()

        with self.assertRaises(StartRoundException) as ctx:
            start_round(session=session, args=StartRoundArgs(user_id="u1"))

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertEqual(ctx.exception.message, "Failed to start round")
