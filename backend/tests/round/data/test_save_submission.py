import unittest
from unittest.mock import create_autospec, patch

from sqlalchemy.orm import Session

from app.round.data.save_submission import save_submission


class TestSaveSubmission(unittest.TestCase):
    @patch("app.round.data.save_submission.save_attempt", autospec=True)
    @patch("app.round.data.save_submission.save_prompt", autospec=True)
    @patch("app.round.data.save_submission.get_or_create_image", autospec=True)
    def test_persists_entities_and_commits(
        self,
        mock_get_or_create_image,
        mock_save_prompt,
        mock_save_attempt,
    ):
        session = create_autospec(Session, instance=True, spec_set=True)
        mock_get_or_create_image.return_value = "img1"
        mock_save_prompt.return_value = "p1"

        save_submission(
            session=session,
            user_id="u1",
            reference_image="golden-sunset.jpeg",
            difficulty="easy",
            prompt_text="a prompt",
            round_id="golden-sunset",
            generated_image_url="https://example.com/generated.jpg",
            similarity_score=50.0,
        )

        mock_get_or_create_image.assert_called_once_with(
            session=session,
            reference_image="golden-sunset.jpeg",
            difficulty="easy",
        )
        mock_save_prompt.assert_called_once_with(
            session=session,
            user_id="u1",
            image_id="img1",
            prompt_text="a prompt",
        )
        mock_save_attempt.assert_called_once_with(
            session=session,
            user_id="u1",
            image_id="img1",
            prompt_id="p1",
            round_id="golden-sunset",
            generated_image_url="https://example.com/generated.jpg",
            similarity_score=50.0,
        )
        session.commit.assert_called_once_with()
