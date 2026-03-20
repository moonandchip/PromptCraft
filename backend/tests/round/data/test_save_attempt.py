import unittest
from unittest.mock import create_autospec, patch

from sqlalchemy.orm import Session

from app.round.data.save_attempt import save_attempt


class TestSaveAttempt(unittest.TestCase):
    @patch("app.round.data.save_attempt.get_next_attempt_number", autospec=True)
    def test_creates_attempt_and_returns_id(self, mock_get_next_attempt_number):
        session = create_autospec(Session, instance=True, spec_set=True)
        mock_get_next_attempt_number.return_value = 2

        attempt_id = save_attempt(
            session=session,
            user_id="u1",
            image_id="img1",
            prompt_id="p1",
            round_id="ancient-temple",
            generated_image_url="https://example.com/generated.jpg",
            similarity_score=50.0,
        )

        self.assertIsInstance(attempt_id, str)
        session.add.assert_called_once()
        session.flush.assert_called_once_with()
        mock_get_next_attempt_number.assert_called_once_with(
            session=session,
            user_id="u1",
            round_id="ancient-temple",
        )

    @patch("app.round.data.save_attempt.get_next_attempt_number", autospec=True)
    def test_attempt_stores_round_id_and_generated_image_url(self, mock_get_next_attempt_number):
        session = create_autospec(Session, instance=True, spec_set=True)
        mock_get_next_attempt_number.return_value = 1

        save_attempt(
            session=session,
            user_id="u1",
            image_id="img1",
            prompt_id="p1",
            round_id="golden-sunset",
            generated_image_url="https://example.com/output.png",
            similarity_score=75.0,
        )

        added_attempt = session.add.call_args[0][0]
        self.assertEqual(added_attempt.round_id, "golden-sunset")
        self.assertEqual(added_attempt.generated_image_url, "https://example.com/output.png")
        self.assertEqual(added_attempt.attempt_number, 1)
