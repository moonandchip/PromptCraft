"""Tests for app.round.transport.submit endpoint functions."""

import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app.round.constants import ROUNDS
from app.round.models import SubmitRequest
from app.round.service.generate_image import GenerationError
from app.round.transport.submit import get_rounds_endpoint, submit_endpoint


_VALID_ROUND_ID = ROUNDS[0]["id"]


class TestGetRoundsEndpoint(unittest.TestCase):
    def test_returns_a_list(self):
        result = get_rounds_endpoint()
        self.assertIsInstance(result, list)

    def test_returns_all_rounds(self):
        result = get_rounds_endpoint()
        self.assertEqual(len(result), len(ROUNDS))

    def test_each_item_has_id(self):
        for item in get_rounds_endpoint():
            self.assertTrue(hasattr(item, "id"))

    def test_each_item_has_title(self):
        for item in get_rounds_endpoint():
            self.assertTrue(hasattr(item, "title"))

    def test_each_item_has_difficulty(self):
        for item in get_rounds_endpoint():
            self.assertTrue(hasattr(item, "difficulty"))

    def test_each_item_has_reference_image(self):
        for item in get_rounds_endpoint():
            self.assertTrue(hasattr(item, "reference_image"))

    def test_round_ids_match_constants(self):
        result_ids = {item.id for item in get_rounds_endpoint()}
        expected_ids = {r["id"] for r in ROUNDS}
        self.assertEqual(result_ids, expected_ids)


class TestSubmitEndpoint(unittest.TestCase):
    @patch("app.round.transport.submit.compute_similarity_score")
    @patch("app.round.transport.submit.generate_image")
    def test_success_returns_image_url(self, mock_generate, mock_clip):
        mock_generate.return_value = "https://example.com/generated.jpg"
        mock_clip.return_value = 72.5
        body = SubmitRequest(round_id=_VALID_ROUND_ID, user_prompt="a majestic scene")

        response = submit_endpoint(body)

        self.assertEqual(response.generated_image_url, "https://example.com/generated.jpg")

    @patch("app.round.transport.submit.compute_similarity_score")
    @patch("app.round.transport.submit.generate_image")
    def test_success_returns_similarity_score(self, mock_generate, mock_clip):
        mock_generate.return_value = "https://example.com/generated.jpg"
        mock_clip.return_value = 72.5
        body = SubmitRequest(round_id=_VALID_ROUND_ID, user_prompt="a majestic scene")

        response = submit_endpoint(body)

        self.assertEqual(response.similarity_score, 72.5)

    def test_unknown_round_id_raises_404(self):
        body = SubmitRequest(round_id="non-existent-round", user_prompt="some prompt")

        with self.assertRaises(HTTPException) as ctx:
            submit_endpoint(body)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_unknown_round_id_error_detail(self):
        from app.round.constants import ERR_ROUND_NOT_FOUND

        body = SubmitRequest(round_id="non-existent-round", user_prompt="some prompt")

        with self.assertRaises(HTTPException) as ctx:
            submit_endpoint(body)
        self.assertEqual(ctx.exception.detail, ERR_ROUND_NOT_FOUND)

    @patch("app.round.transport.submit.generate_image")
    def test_generation_error_propagates_status_code(self, mock_generate):
        mock_generate.side_effect = GenerationError(502, "Image generation failed")
        body = SubmitRequest(round_id=_VALID_ROUND_ID, user_prompt="a prompt")

        with self.assertRaises(HTTPException) as ctx:
            submit_endpoint(body)
        self.assertEqual(ctx.exception.status_code, 502)

    @patch("app.round.transport.submit.generate_image")
    def test_generation_error_propagates_detail(self, mock_generate):
        mock_generate.side_effect = GenerationError(502, "Image generation failed")
        body = SubmitRequest(round_id=_VALID_ROUND_ID, user_prompt="a prompt")

        with self.assertRaises(HTTPException) as ctx:
            submit_endpoint(body)
        self.assertEqual(ctx.exception.detail, "Image generation failed")

    @patch("app.round.transport.submit.compute_similarity_score")
    @patch("app.round.transport.submit.generate_image")
    def test_clip_failure_returns_zero_score(self, mock_generate, mock_clip):
        mock_generate.return_value = "https://example.com/generated.jpg"
        mock_clip.side_effect = Exception("CLIP model unavailable")
        body = SubmitRequest(round_id=_VALID_ROUND_ID, user_prompt="a scene")

        response = submit_endpoint(body)

        self.assertEqual(response.similarity_score, 0.0)

    @patch("app.round.transport.submit.compute_similarity_score")
    @patch("app.round.transport.submit.generate_image")
    def test_clip_failure_still_returns_image_url(self, mock_generate, mock_clip):
        mock_generate.return_value = "https://example.com/generated.jpg"
        mock_clip.side_effect = Exception("CLIP model unavailable")
        body = SubmitRequest(round_id=_VALID_ROUND_ID, user_prompt="a scene")

        response = submit_endpoint(body)

        self.assertEqual(response.generated_image_url, "https://example.com/generated.jpg")

    @patch("app.round.transport.submit.compute_similarity_score")
    @patch("app.round.transport.submit.generate_image")
    def test_generate_image_called_with_user_prompt(self, mock_generate, mock_clip):
        mock_generate.return_value = "https://example.com/img.jpg"
        mock_clip.return_value = 50.0
        body = SubmitRequest(round_id=_VALID_ROUND_ID, user_prompt="a unique test prompt")

        submit_endpoint(body)

        mock_generate.assert_called_once_with("a unique test prompt")
