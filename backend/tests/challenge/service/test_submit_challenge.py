import importlib
import unittest
from unittest.mock import MagicMock, patch

from app.challenge.exceptions import SubmitChallengeException
from app.challenge.types.args import SubmitChallengeArgs
from app.round.service.generate_image import GenerationError

module = importlib.import_module("app.challenge.service.submit_challenge")


def _challenge(max_attempts=3, round_id="ancient-temple"):
    challenge = MagicMock()
    challenge.id = "c-1"
    challenge.round_id = round_id
    challenge.max_attempts = max_attempts
    return challenge


def _args(user_prompt="a vivid scene"):
    return SubmitChallengeArgs(
        user_id="u1",
        user_email="user@example.com",
        user_prompt=user_prompt,
        user_display_name="User",
    )


class TestSubmitChallenge(unittest.TestCase):
    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "save_attempt", autospec=True)
    @patch.object(module, "save_prompt", autospec=True)
    @patch.object(module, "get_or_create_image", autospec=True)
    @patch.object(module, "upsert_user_profile", autospec=True)
    @patch.object(module, "compute_similarity_score", autospec=True)
    @patch.object(module, "generate_image", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_returns_response_on_success(
        self,
        mock_get_or_create,
        mock_get_round,
        mock_generate_image,
        mock_compute,
        mock_upsert,
        mock_get_or_create_image,
        mock_save_prompt,
        mock_save_attempt,
        mock_get_progress,
    ):
        mock_get_or_create.return_value = _challenge()
        mock_get_round.return_value = {
            "id": "ancient-temple",
            "difficulty": "medium",
            "reference_image": "ancient-temple.jpg",
        }
        mock_get_progress.side_effect = [(0, 0.0), (1, 73.2)]
        mock_generate_image.return_value = "https://example.com/g.jpg"
        mock_compute.return_value = 73.2
        mock_get_or_create_image.return_value = "img-1"
        mock_save_prompt.return_value = "prompt-1"
        session = MagicMock()

        response = module.submit_challenge(session=session, args=_args())

        self.assertEqual(response.generated_image_url, "https://example.com/g.jpg")
        self.assertEqual(response.similarity_score, 73.2)
        self.assertEqual(response.attempts_used, 1)
        self.assertEqual(response.attempts_remaining, 2)
        self.assertEqual(response.best_score, 73.2)
        kwargs = mock_save_attempt.call_args.kwargs
        self.assertEqual(kwargs["challenge_id"], "c-1")
        self.assertEqual(kwargs["round_id"], "ancient-temple")
        session.commit.assert_called_once_with()

    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_round_not_found_raises_404(self, mock_get_or_create, mock_get_round):
        mock_get_or_create.return_value = _challenge(round_id="missing")
        mock_get_round.return_value = None

        with self.assertRaises(SubmitChallengeException) as ctx:
            module.submit_challenge(session=MagicMock(), args=_args())

        self.assertEqual(ctx.exception.status_code, 404)

    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_attempt_limit_reached_raises_429(self, mock_get_or_create, mock_get_round, mock_get_progress):
        mock_get_or_create.return_value = _challenge(max_attempts=3)
        mock_get_round.return_value = {"id": "ancient-temple", "difficulty": "medium", "reference_image": "x.jpg"}
        mock_get_progress.return_value = (3, 80.0)

        with self.assertRaises(SubmitChallengeException) as ctx:
            module.submit_challenge(session=MagicMock(), args=_args())

        self.assertEqual(ctx.exception.status_code, 429)

    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "generate_image", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_generation_failure_maps_to_502(self, mock_get_or_create, mock_get_round, mock_generate_image, mock_get_progress):
        mock_get_or_create.return_value = _challenge()
        mock_get_round.return_value = {"id": "ancient-temple", "difficulty": "medium", "reference_image": "x.jpg"}
        mock_get_progress.return_value = (0, 0.0)
        mock_generate_image.side_effect = GenerationError(502, "boom")

        with self.assertRaises(SubmitChallengeException) as ctx:
            module.submit_challenge(session=MagicMock(), args=_args())

        self.assertEqual(ctx.exception.status_code, 502)

    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "generate_image", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_generation_timeout_maps_to_504(self, mock_get_or_create, mock_get_round, mock_generate_image, mock_get_progress):
        mock_get_or_create.return_value = _challenge()
        mock_get_round.return_value = {"id": "ancient-temple", "difficulty": "medium", "reference_image": "x.jpg"}
        mock_get_progress.return_value = (0, 0.0)
        mock_generate_image.side_effect = GenerationError(504, "timed out")

        with self.assertRaises(SubmitChallengeException) as ctx:
            module.submit_challenge(session=MagicMock(), args=_args())

        self.assertEqual(ctx.exception.status_code, 504)

    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "save_attempt", autospec=True)
    @patch.object(module, "save_prompt", autospec=True)
    @patch.object(module, "get_or_create_image", autospec=True)
    @patch.object(module, "upsert_user_profile", autospec=True)
    @patch.object(module, "compute_similarity_score", autospec=True)
    @patch.object(module, "generate_image", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_clip_failure_persists_zero_score(
        self,
        mock_get_or_create,
        mock_get_round,
        mock_generate_image,
        mock_compute,
        mock_upsert,
        mock_get_or_create_image,
        mock_save_prompt,
        mock_save_attempt,
        mock_get_progress,
    ):
        mock_get_or_create.return_value = _challenge()
        mock_get_round.return_value = {"id": "ancient-temple", "difficulty": "medium", "reference_image": "x.jpg"}
        mock_get_progress.side_effect = [(0, 0.0), (1, 0.0)]
        mock_generate_image.return_value = "https://example.com/g.jpg"
        mock_compute.side_effect = Exception("CLIP unavailable")
        mock_get_or_create_image.return_value = "img-1"
        mock_save_prompt.return_value = "prompt-1"

        response = module.submit_challenge(session=MagicMock(), args=_args())

        self.assertEqual(response.similarity_score, 0.0)
        kwargs = mock_save_attempt.call_args.kwargs
        self.assertEqual(kwargs["similarity_score"], 0.0)

    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "save_attempt", autospec=True)
    @patch.object(module, "save_prompt", autospec=True)
    @patch.object(module, "get_or_create_image", autospec=True)
    @patch.object(module, "upsert_user_profile", autospec=True)
    @patch.object(module, "compute_similarity_score", autospec=True)
    @patch.object(module, "generate_image", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_persistence_failure_rolls_back_and_maps_to_500(
        self,
        mock_get_or_create,
        mock_get_round,
        mock_generate_image,
        mock_compute,
        mock_upsert,
        mock_get_or_create_image,
        mock_save_prompt,
        mock_save_attempt,
        mock_get_progress,
    ):
        mock_get_or_create.return_value = _challenge()
        mock_get_round.return_value = {"id": "ancient-temple", "difficulty": "medium", "reference_image": "x.jpg"}
        mock_get_progress.return_value = (0, 0.0)
        mock_generate_image.return_value = "https://example.com/g.jpg"
        mock_compute.return_value = 50.0
        mock_get_or_create_image.return_value = "img-1"
        mock_save_prompt.return_value = "prompt-1"
        mock_save_attempt.side_effect = Exception("DB down")
        session = MagicMock()

        with self.assertRaises(SubmitChallengeException) as ctx:
            module.submit_challenge(session=session, args=_args())

        self.assertEqual(ctx.exception.status_code, 500)
        session.rollback.assert_called_once_with()

    @patch.object(module, "get_user_challenge_progress", autospec=True)
    @patch.object(module, "save_attempt", autospec=True)
    @patch.object(module, "save_prompt", autospec=True)
    @patch.object(module, "get_or_create_image", autospec=True)
    @patch.object(module, "upsert_user_profile", autospec=True)
    @patch.object(module, "compute_similarity_score", autospec=True)
    @patch.object(module, "generate_image", autospec=True)
    @patch.object(module, "get_round_by_id", autospec=True)
    @patch.object(module, "get_or_create_current_challenge", autospec=True)
    def test_attempts_remaining_never_negative(
        self,
        mock_get_or_create,
        mock_get_round,
        mock_generate_image,
        mock_compute,
        mock_upsert,
        mock_get_or_create_image,
        mock_save_prompt,
        mock_save_attempt,
        mock_get_progress,
    ):
        mock_get_or_create.return_value = _challenge(max_attempts=1)
        mock_get_round.return_value = {"id": "ancient-temple", "difficulty": "medium", "reference_image": "x.jpg"}
        mock_get_progress.side_effect = [(0, 0.0), (5, 80.0)]
        mock_generate_image.return_value = "https://example.com/g.jpg"
        mock_compute.return_value = 80.0
        mock_get_or_create_image.return_value = "img-1"
        mock_save_prompt.return_value = "prompt-1"

        response = module.submit_challenge(session=MagicMock(), args=_args())

        self.assertEqual(response.attempts_remaining, 0)
