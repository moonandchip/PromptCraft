import unittest
from unittest.mock import MagicMock, patch

from app.round.exceptions import RoundError, SubmitRoundException
from app.round.service.generate_image import GenerationError
from app.round.service.submit_round import submit_round


class TestSubmitRound(unittest.TestCase):
    @patch("app.round.service.submit_round.save_submission", autospec=True)
    @patch("app.round.service.submit_round.compute_similarity_score", autospec=True)
    @patch("app.round.service.submit_round.generate_image", autospec=True)
    @patch("app.round.service.submit_round.get_round_by_id", autospec=True)
    def test_submit_round_returns_response_on_success(
        self,
        mock_get_round_by_id,
        mock_generate_image,
        mock_compute_similarity_score,
        mock_save_submission,
    ):
        session = MagicMock()
        mock_get_round_by_id.return_value = {
            "id": "ancient-temple",
            "difficulty": "medium",
            "reference_image": "ancient-temple.jpg",
        }
        mock_generate_image.return_value = "https://example.com/generated.jpg"
        mock_compute_similarity_score.return_value = 72.5

        response = submit_round(
            session=session,
            user_email="test@example.com",
            round_id="ancient-temple",
            user_prompt="a majestic scene",
        )

        self.assertEqual(response.generated_image_url, "https://example.com/generated.jpg")
        self.assertEqual(response.similarity_score, 72.5)
        mock_save_submission.assert_called_once_with(
            session=session,
            user_email="test@example.com",
            reference_image="ancient-temple.jpg",
            difficulty="medium",
            prompt_text="a majestic scene",
            round_id="ancient-temple",
            generated_image_url="https://example.com/generated.jpg",
            similarity_score=72.5,
        )

    @patch("app.round.service.submit_round.get_round_by_id", autospec=True)
    def test_submit_round_raises_not_found_error(self, mock_get_round_by_id):
        mock_get_round_by_id.return_value = None

        with self.assertRaises(SubmitRoundException) as ctx:
            submit_round(
                session=MagicMock(),
                user_email="test@example.com",
                round_id="missing-round",
                user_prompt="prompt",
            )

        self.assertEqual(ctx.exception.status_code, 404)

    @patch("app.round.service.submit_round.generate_image", autospec=True)
    @patch("app.round.service.submit_round.get_round_by_id", autospec=True)
    def test_submit_round_maps_generation_error(self, mock_get_round_by_id, mock_generate_image):
        mock_get_round_by_id.return_value = {
            "id": "ancient-temple",
            "difficulty": "medium",
            "reference_image": "ancient-temple.jpg",
        }
        mock_generate_image.side_effect = GenerationError(502, "Image generation failed")

        with self.assertRaises(SubmitRoundException) as ctx:
            submit_round(
                session=MagicMock(),
                user_email="test@example.com",
                round_id="ancient-temple",
                user_prompt="prompt",
            )

        self.assertEqual(ctx.exception.status_code, 502)
        self.assertEqual(ctx.exception.message, "Image generation failed")

    @patch("app.round.service.submit_round.save_submission", autospec=True)
    @patch("app.round.service.submit_round.compute_similarity_score", autospec=True)
    @patch("app.round.service.submit_round.generate_image", autospec=True)
    @patch("app.round.service.submit_round.get_round_by_id", autospec=True)
    def test_submit_round_uses_zero_score_when_clip_fails(
        self,
        mock_get_round_by_id,
        mock_generate_image,
        mock_compute_similarity_score,
        mock_save_submission,
    ):
        session = MagicMock()
        mock_get_round_by_id.return_value = {
            "id": "ancient-temple",
            "difficulty": "medium",
            "reference_image": "ancient-temple.jpg",
        }
        mock_generate_image.return_value = "https://example.com/generated.jpg"
        mock_compute_similarity_score.side_effect = Exception("CLIP unavailable")

        response = submit_round(
            session=session,
            user_email="test@example.com",
            round_id="ancient-temple",
            user_prompt="prompt",
        )

        self.assertEqual(response.similarity_score, 0.0)
        kwargs = mock_save_submission.call_args.kwargs
        self.assertEqual(kwargs["similarity_score"], 0.0)
        self.assertEqual(kwargs["round_id"], "ancient-temple")
        self.assertEqual(kwargs["generated_image_url"], "https://example.com/generated.jpg")

    @patch("app.round.service.submit_round.save_submission", autospec=True)
    @patch("app.round.service.submit_round.compute_similarity_score", autospec=True)
    @patch("app.round.service.submit_round.generate_image", autospec=True)
    @patch("app.round.service.submit_round.get_round_by_id", autospec=True)
    def test_submit_round_maps_persistence_error(
        self,
        mock_get_round_by_id,
        mock_generate_image,
        mock_compute_similarity_score,
        mock_save_submission,
    ):
        mock_get_round_by_id.return_value = {
            "id": "ancient-temple",
            "difficulty": "medium",
            "reference_image": "ancient-temple.jpg",
        }
        mock_generate_image.return_value = "https://example.com/generated.jpg"
        mock_compute_similarity_score.return_value = 50.0
        mock_save_submission.side_effect = Exception("DB unavailable")

        with self.assertRaises(SubmitRoundException) as ctx:
            submit_round(
                session=MagicMock(),
                user_email="test@example.com",
                round_id="ancient-temple",
                user_prompt="prompt",
            )

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertEqual(ctx.exception.message, "Failed to save submission")
