"""LLM-based prompt feedback using OpenAI vision models.

Sends the reference image and the user's prompt to a vision-capable LLM,
which returns actionable feedback on how to improve the prompt.
"""

from __future__ import annotations

import base64
import logging
import os
from pathlib import Path

from openai import OpenAI

from ..constants import CHANNEL

logger = logging.getLogger(__name__)

_FEEDBACK_MODEL_ENV_VAR = "PROMPT_FEEDBACK_MODEL"
_OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"
_DEFAULT_MODEL = "gpt-4.1-mini"

_SYSTEM_PROMPT = """\
You are a prompt-engineering coach for an AI image generation game.

The user is trying to write a text prompt that will make an AI generate an image \
matching a reference image as closely as possible.

You will receive:
1. The reference image the user is trying to match.
2. The text prompt the user wrote.
3. The similarity score (0-100) their generated image achieved.

Provide 2-4 concise, actionable bullet points on how to improve the prompt.
At least 1 bullet point must be a general prompt-engineering tip that helps the user write better image prompts overall, not just for this specific image.

Focus on:
- Key visual elements in the reference image that the prompt missed or described inaccurately.
- Specificity: vague descriptions that could be made more precise.
- Style, mood, lighting, or composition details visible in the reference image.
- Spatial relationships or layout details that would help the AI.
- General prompt-writing advice such as adding subject details, composition, lighting, camera angle, style, or clearer spatial relationships.

Keep each bullet point to 1-2 sentences. Be encouraging but specific. \
Do NOT describe the reference image exhaustively — only mention what's relevant to improving the prompt.\
"""


def _encode_image_to_base64(path: Path) -> str:
    """Read a local image file and return its base64-encoded content."""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def _get_mime_type(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(suffix, "image/jpeg")


def generate_prompt_feedback(
    reference_image_path: Path,
    user_prompt: str,
    similarity_score: float,
) -> list[str]:
    """Return a list of feedback bullet points for the user's prompt.

    Parameters
    ----------
    reference_image_path:
        Absolute path to the local reference image.
    user_prompt:
        The text prompt the user submitted.
    similarity_score:
        The CLIP similarity score (0-100) the attempt achieved.

    Returns
    -------
    list[str]
        A list of 2-4 actionable feedback strings, or an empty list on failure.
    """
    api_key = os.environ.get(_OPENAI_API_KEY_ENV_VAR, "").strip()
    if not api_key:
        logger.warning("OpenAI API key not set; skipping prompt feedback")
        return []

    model = os.environ.get(_FEEDBACK_MODEL_ENV_VAR, _DEFAULT_MODEL).strip()

    image_b64 = _encode_image_to_base64(reference_image_path)
    mime_type = _get_mime_type(reference_image_path)

    user_message = (
        f"**User's prompt:** {user_prompt}\n\n"
        f"**Similarity score:** {similarity_score:.1f} / 100"
    )

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_b64}",
                                "detail": "low",
                            },
                        },
                        {"type": "text", "text": user_message},
                    ],
                },
            ],
            max_tokens=400,
            temperature=0.7,
        )

        raw_text = response.choices[0].message.content or ""
        # Parse bullet points: lines starting with - or *
        bullets = []
        for line in raw_text.strip().splitlines():
            stripped = line.strip()
            if stripped.startswith(("- ", "* ", "• ")):
                stripped = stripped.lstrip("-*• ").strip()
            if stripped:
                bullets.append(stripped)

        return bullets if bullets else [raw_text.strip()]

    except Exception as exc:
        logger.error(
            "Prompt feedback generation failed",
            extra={"channel": CHANNEL, "error": str(exc)},
        )
        return []
