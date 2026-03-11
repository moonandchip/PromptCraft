"""CLIP-based image similarity scoring.

Compares a generated image against a reference image using OpenAI's
CLIP model.  Returns a normalised 0–100 score where higher
means the two images are more visually similar.

Flow:
  1. Load / cache the CLIP model + processor on first call.
  2. Download the generated image from its URL.
  3. Open the local reference image from disk.
  4. Compute CLIP image embeddings for both.
  5. Return cosine-similarity mapped to [0, 100].
"""

from __future__ import annotations

import io
import logging
import urllib.request
from pathlib import Path

import torch  # type: ignore[import-untyped]
from PIL import Image
from transformers import CLIPModel, CLIPProcessor  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


_model: CLIPModel | None = None
_processor: CLIPProcessor | None = None
_CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"


def _get_model_and_processor() -> tuple[CLIPModel, CLIPProcessor]:
    """Lazy-load the CLIP model and processor (downloads on first run)."""
    global _model, _processor  # noqa: PLW0603
    if _model is None or _processor is None:
        logger.info("Loading CLIP model '%s' …", _CLIP_MODEL_NAME)
        _model = CLIPModel.from_pretrained(_CLIP_MODEL_NAME)
        _processor = CLIPProcessor.from_pretrained(_CLIP_MODEL_NAME)
        _model.eval()
        logger.info("CLIP model loaded successfully.")
    return _model, _processor


# Image helpers

def _load_image_from_url(url: str) -> Image.Image:
    """Download an image from *url* and return a PIL Image in RGB."""
    req = urllib.request.Request(url, headers={"User-Agent": "PromptCraft/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
        data = resp.read()
    return Image.open(io.BytesIO(data)).convert("RGB")


def _load_image_from_path(path: str | Path) -> Image.Image:
    """Open a local image file and return a PIL Image in RGB."""
    return Image.open(path).convert("RGB")


# Public API

def compute_similarity_score(
    reference_image_path: str | Path,
    generated_image_url: str,
) -> float:
    """Return a similarity score in **[0, 100]** for two images.

    Parameters
    ----------
    reference_image_path:
        Absolute path to the local reference image file.
    generated_image_url:
        URL of the AI-generated image.

    Returns
    -------
    float
        Cosine-similarity of the two CLIP embeddings, mapped to 0–100 and
        rounded to one decimal place.
    """
    model, processor = _get_model_and_processor()

    # Load both images
    reference_img = _load_image_from_path(reference_image_path)
    generated_img = _load_image_from_url(generated_image_url)

    # Compute CLIP image embeddings
    inputs = processor(images=[reference_img, generated_img], return_tensors="pt")

    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    # Normalise embeddings to unit vectors
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    # Cosine similarity (dot product of unit vectors)
    cosine_sim: float = (image_features[0] @ image_features[1]).item()

    # CLIP cosine similarities for images typically range from ~0.5 to ~1.0.
    # Map that range to 0–100 so scores are intuitive.
    score = max(0.0, min((cosine_sim - 0.5) * 200.0, 100.0))

    score = round(score, 1)
    logger.info(
        "CLIP similarity  raw=%.4f  score=%.1f  ref=%s",
        cosine_sim,
        score,
        Path(reference_image_path).name,
    )
    return score
