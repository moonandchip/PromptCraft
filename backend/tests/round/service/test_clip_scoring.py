"""Tests for app.round.service.clip_scoring.

These tests mock the heavy ML dependencies (torch, transformers) so they
run in any environment – with or without those packages installed.  The
actual math inside ``compute_similarity_score`` is exercised by
configuring the MagicMock chain to return a controlled float from
``image_features[i] @ image_features[j]).item()``.

Tensor-operation chain traced through clip_scoring.py
------------------------------------------------------
    image_features  = model.get_image_features(**inputs)       # feat_mock
    image_features  = image_features / image_features.norm(…)  # feat_mock.__truediv__.rv
    cosine_sim      = (image_features[0] @ image_features[1]).item()
                      └─ [0] → __getitem__.rv
                      └─ @ …  → __matmul__.rv
                      └─ .item() → configured float value
"""

import io
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from PIL import Image

from app.round.service.clip_scoring import (
    _load_image_from_path,
    _load_image_from_url,
    compute_similarity_score,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_dummy_rgb_image(width: int = 10, height: int = 10) -> Image.Image:
    """Create a small dummy RGB image for testing."""
    return Image.new("RGB", (width, height), color=(128, 64, 32))


def _image_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def _build_feature_mock(cosine_sim_value: float) -> MagicMock:
    """Return a MagicMock that mimics a (2, d) tensor with a controlled cosine sim.

    The mock is wired so that the chain executed inside
    ``compute_similarity_score`` resolves to *cosine_sim_value*:

        (norm_feat[0] @ norm_feat[1]).item()  →  cosine_sim_value
    """
    feat = MagicMock()
    # feat / feat.norm(…)  →  norm_feat
    norm_feat = feat.__truediv__.return_value
    # norm_feat[i]  →  elem  (same MagicMock for both indices – sufficient here)
    elem = norm_feat.__getitem__.return_value
    # elem @ elem  →  dot_result
    dot_result = elem.__matmul__.return_value
    # dot_result.item()  →  the desired float
    dot_result.item.return_value = cosine_sim_value
    return feat


def _make_mock_model_and_processor(cosine_sim_value: float):
    mock_model = MagicMock()
    mock_processor = MagicMock()
    mock_processor.return_value = {}
    mock_model.get_image_features.return_value = _build_feature_mock(cosine_sim_value)
    return mock_model, mock_processor


# ---------------------------------------------------------------------------
# _load_image_from_url
# ---------------------------------------------------------------------------

class TestLoadImageFromUrl(unittest.TestCase):
    @patch("app.round.service.clip_scoring.urllib.request.urlopen")
    def test_returns_rgb_image(self, mock_urlopen):
        img = _make_dummy_rgb_image()
        cm = MagicMock()
        cm.__enter__ = lambda s: s
        cm.__exit__ = MagicMock(return_value=False)
        cm.read.return_value = _image_to_bytes(img)
        mock_urlopen.return_value = cm

        result = _load_image_from_url("https://example.com/image.jpg")

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGB")

    @patch("app.round.service.clip_scoring.urllib.request.urlopen")
    def test_converts_greyscale_to_rgb(self, mock_urlopen):
        grey = Image.new("L", (10, 10), color=128)
        cm = MagicMock()
        cm.__enter__ = lambda s: s
        cm.__exit__ = MagicMock(return_value=False)
        cm.read.return_value = _image_to_bytes(grey)
        mock_urlopen.return_value = cm

        result = _load_image_from_url("https://example.com/grey.png")

        self.assertEqual(result.mode, "RGB")

    @patch("app.round.service.clip_scoring.urllib.request.urlopen")
    def test_converts_rgba_to_rgb(self, mock_urlopen):
        rgba = Image.new("RGBA", (10, 10), color=(128, 64, 32, 200))
        cm = MagicMock()
        cm.__enter__ = lambda s: s
        cm.__exit__ = MagicMock(return_value=False)
        cm.read.return_value = _image_to_bytes(rgba)
        mock_urlopen.return_value = cm

        result = _load_image_from_url("https://example.com/rgba.png")

        self.assertEqual(result.mode, "RGB")


# ---------------------------------------------------------------------------
# _load_image_from_path
# ---------------------------------------------------------------------------

class TestLoadImageFromPath(unittest.TestCase):
    def test_loads_image_and_returns_rgb(self):
        img = _make_dummy_rgb_image()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            img.save(f.name, format="PNG")
            result = _load_image_from_path(f.name)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGB")

    def test_accepts_pathlib_path(self):
        from pathlib import Path

        img = _make_dummy_rgb_image()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            img.save(f.name, format="PNG")
            result = _load_image_from_path(Path(f.name))

        self.assertIsInstance(result, Image.Image)

    def test_converts_greyscale_to_rgb(self):
        grey = Image.new("L", (10, 10), color=100)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            grey.save(f.name, format="PNG")
            result = _load_image_from_path(f.name)

        self.assertEqual(result.mode, "RGB")


# ---------------------------------------------------------------------------
# compute_similarity_score
# ---------------------------------------------------------------------------

class TestComputeSimilarityScore(unittest.TestCase):
    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_returns_float(self, mock_get_model, mock_load_path, mock_load_url):
        mock_get_model.return_value = _make_mock_model_and_processor(0.8)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        score = compute_similarity_score("ref.png", "https://example.com/gen.jpg")

        self.assertIsInstance(score, float)

    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_score_is_within_0_to_100(self, mock_get_model, mock_load_path, mock_load_url):
        mock_get_model.return_value = _make_mock_model_and_processor(0.8)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        score = compute_similarity_score("ref.png", "https://example.com/gen.jpg")

        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)

    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_identical_images_yield_score_100(self, mock_get_model, mock_load_path, mock_load_url):
        """Cosine similarity of 1.0 should map to score 100."""
        mock_get_model.return_value = _make_mock_model_and_processor(1.0)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        score = compute_similarity_score("ref.png", "https://example.com/gen.jpg")

        self.assertEqual(score, 100.0)

    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_dissimilar_images_yield_score_0(self, mock_get_model, mock_load_path, mock_load_url):
        """Cosine similarity of -1.0 (opposite vectors) should map to score 0."""
        mock_get_model.return_value = _make_mock_model_and_processor(-1.0)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        score = compute_similarity_score("ref.png", "https://example.com/gen.jpg")

        self.assertEqual(score, 0.0)

    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_boundary_cosine_sim_0_5_yields_score_0(self, mock_get_model, mock_load_path, mock_load_url):
        """cos_sim = 0.5 → (0.5 - 0.5) * 200 = 0.0."""
        mock_get_model.return_value = _make_mock_model_and_processor(0.5)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        score = compute_similarity_score("ref.png", "https://example.com/gen.jpg")

        self.assertEqual(score, 0.0)

    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_midpoint_cosine_sim_yields_correct_score(self, mock_get_model, mock_load_path, mock_load_url):
        """cos_sim = 0.75 → (0.75 - 0.5) * 200 = 50.0."""
        mock_get_model.return_value = _make_mock_model_and_processor(0.75)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        score = compute_similarity_score("ref.png", "https://example.com/gen.jpg")

        self.assertEqual(score, 50.0)

    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_score_is_rounded_to_one_decimal(self, mock_get_model, mock_load_path, mock_load_url):
        # cos_sim = 0.6 → (0.6 - 0.5) * 200 = 20.0 (exactly 1 dp)
        mock_get_model.return_value = _make_mock_model_and_processor(0.6)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        score = compute_similarity_score("ref.png", "https://example.com/gen.jpg")

        self.assertEqual(round(score, 1), score)

    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_calls_load_path_with_reference(self, mock_get_model, mock_load_path, mock_load_url):
        mock_get_model.return_value = _make_mock_model_and_processor(0.8)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        compute_similarity_score("my/ref.png", "https://example.com/gen.jpg")

        mock_load_path.assert_called_once_with("my/ref.png")

    @patch("app.round.service.clip_scoring._load_image_from_url")
    @patch("app.round.service.clip_scoring._load_image_from_path")
    @patch("app.round.service.clip_scoring._get_model_and_processor")
    def test_calls_load_url_with_generated_url(self, mock_get_model, mock_load_path, mock_load_url):
        mock_get_model.return_value = _make_mock_model_and_processor(0.8)
        mock_load_path.return_value = _make_dummy_rgb_image()
        mock_load_url.return_value = _make_dummy_rgb_image()

        compute_similarity_score("ref.png", "https://example.com/my-gen.jpg")

        mock_load_url.assert_called_once_with("https://example.com/my-gen.jpg")
