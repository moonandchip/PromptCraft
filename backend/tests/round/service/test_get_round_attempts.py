import unittest
from unittest.mock import create_autospec, patch

from sqlalchemy.orm import Session

from app.round.models import AttemptInfo
from app.round.service.get_round_attempts import get_round_attempts


class TestGetRoundAttempts(unittest.TestCase):
    @patch("app.round.service.get_round_attempts.get_attempts_by_round_id", autospec=True)
    def test_maps_data_rows_to_attempt_info_models(self, mock_get_attempts_by_round_id):
        session = create_autospec(Session, instance=True, spec_set=True)
        mock_get_attempts_by_round_id.return_value = [
            (1, "first prompt", "https://example.com/first.png", 45.0),
            (2, "second prompt", "https://example.com/second.png", 78.5),
        ]

        attempts = get_round_attempts(session=session, user_id="u1", round_id="ancient-temple")

        self.assertEqual(
            attempts,
            [
                AttemptInfo(
                    attempt_number=1,
                    prompt="first prompt",
                    generated_image_url="https://example.com/first.png",
                    similarity_score=45.0,
                ),
                AttemptInfo(
                    attempt_number=2,
                    prompt="second prompt",
                    generated_image_url="https://example.com/second.png",
                    similarity_score=78.5,
                ),
            ],
        )
        mock_get_attempts_by_round_id.assert_called_once_with(
            session=session,
            user_id="u1",
            round_id="ancient-temple",
        )
