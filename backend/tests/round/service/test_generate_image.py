"""Tests for app.round.service.generate_image."""

import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from app.round.service.generate_image import (
    GenerationError,
    _extract_image_url,
    _make_request,
    generate_image,
)


class TestGenerationError(unittest.TestCase):
    def test_sets_status_code(self):
        err = GenerationError(502, "Image generation failed")
        self.assertEqual(err.status_code, 502)

    def test_sets_detail(self):
        err = GenerationError(500, "API key not configured")
        self.assertEqual(err.detail, "API key not configured")

    def test_is_exception_subclass(self):
        err = GenerationError(404, "not found")
        self.assertIsInstance(err, Exception)

    def test_str_representation(self):
        err = GenerationError(503, "timeout")
        self.assertIn("timeout", str(err))


class TestExtractImageUrl(unittest.TestCase):
    def test_extracts_url_from_images_shape(self):
        response = {"images": [{"url": "https://example.com/image.jpg"}]}
        self.assertEqual(_extract_image_url(response), "https://example.com/image.jpg")

    def test_extracts_url_from_generated_images_shape(self):
        response = {"generated_images": [{"url": "https://example.com/image2.jpg"}]}
        self.assertEqual(_extract_image_url(response), "https://example.com/image2.jpg")

    def test_extracts_url_from_data_shape(self):
        response = {"data": [{"url": "https://example.com/image3.jpg"}]}
        self.assertEqual(_extract_image_url(response), "https://example.com/image3.jpg")

    def test_returns_none_when_empty_response(self):
        self.assertIsNone(_extract_image_url({}))

    def test_returns_none_when_images_list_empty(self):
        self.assertIsNone(_extract_image_url({"images": []}))

    def test_returns_none_when_url_field_missing(self):
        self.assertIsNone(_extract_image_url({"images": [{"noturl": "x"}]}))

    def test_returns_none_when_url_is_empty_string(self):
        self.assertIsNone(_extract_image_url({"images": [{"url": ""}]}))

    def test_prefers_images_shape_over_generated_images(self):
        response = {
            "images": [{"url": "https://from-images.com/img.jpg"}],
            "generated_images": [{"url": "https://from-generated.com/img.jpg"}],
        }
        self.assertEqual(_extract_image_url(response), "https://from-images.com/img.jpg")


class TestMakeRequest(unittest.TestCase):
    @patch("app.round.service.generate_image.request.urlopen")
    def test_returns_parsed_json_on_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_resp.read.return_value = b'{"key": "value"}'
        mock_urlopen.return_value = mock_resp

        result = _make_request("GET", "https://example.com", "api-key")
        self.assertEqual(result, {"key": "value"})

    @patch("app.round.service.generate_image.request.urlopen")
    def test_returns_empty_dict_for_empty_response_body(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_resp.read.return_value = b""
        mock_urlopen.return_value = mock_resp

        result = _make_request("GET", "https://example.com", "api-key")
        self.assertEqual(result, {})

    @patch("app.round.service.generate_image.request.urlopen")
    def test_raises_generation_error_on_http_error(self, mock_urlopen):
        exc = HTTPError(
            url="https://example.com", code=401, msg="Unauthorized", hdrs=None, fp=None
        )
        mock_urlopen.side_effect = exc

        with self.assertRaises(GenerationError) as ctx:
            _make_request("GET", "https://example.com", "api-key")
        self.assertEqual(ctx.exception.status_code, 401)

    @patch("app.round.service.generate_image.request.urlopen")
    def test_raises_generation_error_with_502_on_url_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("connection refused")

        with self.assertRaises(GenerationError) as ctx:
            _make_request("GET", "https://example.com", "api-key")
        self.assertEqual(ctx.exception.status_code, 502)


class TestGenerateImage(unittest.TestCase):
    @patch.dict("os.environ", {"LEONARDO_API_KEY": ""})
    def test_raises_500_when_api_key_missing(self):
        with self.assertRaises(GenerationError) as ctx:
            generate_image("a beautiful landscape")
        self.assertEqual(ctx.exception.status_code, 500)

    @patch("app.round.service.generate_image._make_request")
    @patch.dict("os.environ", {"LEONARDO_API_KEY": "test-api-key"})
    def test_returns_url_when_post_returns_images_synchronously(self, mock_make_request):
        mock_make_request.return_value = {"images": [{"url": "https://example.com/image.jpg"}]}
        url = generate_image("a beautiful landscape")
        self.assertEqual(url, "https://example.com/image.jpg")

    @patch("app.round.service.generate_image.time.sleep")
    @patch("app.round.service.generate_image._make_request")
    @patch.dict("os.environ", {"LEONARDO_API_KEY": "test-api-key"})
    def test_polls_and_returns_url_on_complete_status(self, mock_make_request, mock_sleep):
        mock_make_request.side_effect = [
            {"generationId": "gen-123"},
            {
                "generations_by_pk": {
                    "status": "COMPLETE",
                    "generated_images": [{"url": "https://example.com/polled.jpg"}],
                }
            },
        ]
        url = generate_image("a forest scene")
        self.assertEqual(url, "https://example.com/polled.jpg")

    @patch("app.round.service.generate_image.time.sleep")
    @patch("app.round.service.generate_image._make_request")
    @patch.dict("os.environ", {"LEONARDO_API_KEY": "test-api-key"})
    def test_raises_504_after_max_poll_attempts(self, mock_make_request, mock_sleep):
        from app.round.constants import POLL_MAX_ATTEMPTS

        pending_response = {"generations_by_pk": {"status": "PENDING", "generated_images": []}}
        mock_make_request.side_effect = (
            [{"generationId": "gen-timeout"}] + [pending_response] * POLL_MAX_ATTEMPTS
        )

        with self.assertRaises(GenerationError) as ctx:
            generate_image("an ocean scene")
        self.assertEqual(ctx.exception.status_code, 504)

    @patch("app.round.service.generate_image.time.sleep")
    @patch("app.round.service.generate_image._make_request")
    @patch.dict("os.environ", {"LEONARDO_API_KEY": "test-api-key"})
    def test_raises_502_on_failed_generation_status(self, mock_make_request, mock_sleep):
        mock_make_request.side_effect = [
            {"generationId": "gen-fail"},
            {"generations_by_pk": {"status": "FAILED", "generated_images": []}},
        ]
        with self.assertRaises(GenerationError) as ctx:
            generate_image("a sunset scene")
        self.assertEqual(ctx.exception.status_code, 502)

    @patch("app.round.service.generate_image._make_request")
    @patch.dict("os.environ", {"LEONARDO_API_KEY": "test-api-key"})
    def test_raises_502_when_no_generation_id_returned(self, mock_make_request):
        mock_make_request.return_value = {}
        with self.assertRaises(GenerationError) as ctx:
            generate_image("a city scene")
        self.assertEqual(ctx.exception.status_code, 502)

    @patch("app.round.service.generate_image.time.sleep")
    @patch("app.round.service.generate_image._make_request")
    @patch.dict("os.environ", {"LEONARDO_API_KEY": "test-api-key"})
    def test_accepts_generation_id_from_sdgenerationjob_key(self, mock_make_request, mock_sleep):
        mock_make_request.side_effect = [
            {"sdGenerationJob": {"generationId": "job-123"}},
            {
                "generations_by_pk": {
                    "status": "COMPLETE",
                    "generated_images": [{"url": "https://example.com/job.jpg"}],
                }
            },
        ]
        url = generate_image("a winter landscape")
        self.assertEqual(url, "https://example.com/job.jpg")

    @patch("app.round.service.generate_image.time.sleep")
    @patch("app.round.service.generate_image._make_request")
    @patch.dict("os.environ", {"LEONARDO_API_KEY": "test-api-key"})
    def test_returns_url_from_poll_response_images_shape(self, mock_make_request, mock_sleep):
        """If a poll response contains images directly, return immediately."""
        mock_make_request.side_effect = [
            {"generationId": "gen-456"},
            {"images": [{"url": "https://example.com/poll-immediate.jpg"}]},
        ]
        url = generate_image("a mountain scene")
        self.assertEqual(url, "https://example.com/poll-immediate.jpg")
