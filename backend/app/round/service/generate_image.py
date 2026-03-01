import json
import logging
import os
import time
from urllib import error, request

from ..constants import (
    ERR_GENERATION_API_ERROR,
    ERR_GENERATION_FAILED,
    ERR_GENERATION_TIMEOUT,
    ERR_NO_API_KEY,
    GENERATION_HEIGHT,
    GENERATION_MODEL_ID,
    GENERATION_NUM_IMAGES,
    GENERATION_WIDTH,
    LEONARDO_API_V1_BASE_URL,
    LEONARDO_API_V2_BASE_URL,
    LEONARDO_API_KEY_ENV_VAR,
    LEONARDO_GENERATIONS_PATH,
    POLL_INTERVAL_SECONDS,
    POLL_MAX_ATTEMPTS,
)

log = logging.getLogger(__name__)


class GenerationError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def _make_request(method: str, url: str, api_key: str, body: dict | None = None) -> dict:
    """Send an authenticated JSON request to the Leonardo API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = request.Request(url=url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except error.HTTPError as exc:
        raw_err = ""
        try:
            raw_err = exc.read().decode("utf-8")
        except Exception:
            pass
        log.error("Leonardo HTTP %s %s → %s: %s", method, url, exc.code, raw_err)
        detail = ERR_GENERATION_API_ERROR
        try:
            payload = json.loads(raw_err)
            if isinstance(payload, dict):
                detail = str(payload.get("message") or payload.get("detail") or detail)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        raise GenerationError(exc.code, detail) from exc
    except error.URLError as exc:
        raise GenerationError(502, f"{ERR_GENERATION_API_ERROR}: {exc.reason}") from exc


def _extract_image_url(response: dict) -> str | None:
    """Try every known v2 response shape to find a generated image URL."""
    # Shape 1: {"images": [{"url": "..."}]}
    images = response.get("images") or []
    if images and isinstance(images, list):
        url = images[0].get("url", "") if isinstance(images[0], dict) else ""
        if url:
            return url

    # Shape 2: {"generated_images": [{"url": "..."}]}
    gen_images = response.get("generated_images") or []
    if gen_images and isinstance(gen_images, list):
        url = gen_images[0].get("url", "") if isinstance(gen_images[0], dict) else ""
        if url:
            return url

    # Shape 3: {"data": [{"url": "..."}]}
    data = response.get("data") or []
    if data and isinstance(data, list):
        url = data[0].get("url", "") if isinstance(data[0], dict) else ""
        if url:
            return url

    return None


def generate_image(user_prompt: str) -> str:
    """Call Leonardo API to generate an image and return the URL.

    Workflow (v2 / Nano Banana):
    1. POST /v2/generations get a generationId OR receive images immediately.
    2. Poll GET /v1/generations/{id} until generated_images is populated.
    3. Return the URL of the first generated image.
    """
    api_key = os.environ.get(LEONARDO_API_KEY_ENV_VAR, "").strip()
    if not api_key:
        raise GenerationError(500, ERR_NO_API_KEY)

    # Step 1: start generation
    generation_body = {
        "model": GENERATION_MODEL_ID,
        "parameters": {
            "prompt": user_prompt,
            "width": GENERATION_WIDTH,
            "height": GENERATION_HEIGHT,
            "quantity": GENERATION_NUM_IMAGES,
            "prompt_enhance": "OFF",
        },
        "public": False,
    }
    start_url = f"{LEONARDO_API_V2_BASE_URL}{LEONARDO_GENERATIONS_PATH}"
    log.info("Leonardo POST %s model=%s", start_url, GENERATION_MODEL_ID)
    start_response = _make_request("POST", start_url, api_key, body=generation_body)
    log.info("Leonardo POST response keys: %s", list(start_response.keys()))
    log.debug("Leonardo POST full response: %s", json.dumps(start_response))

    # Check if images arrived synchronously in the POST response
    immediate_url = _extract_image_url(start_response)
    if immediate_url:
        log.info("Leonardo returned image synchronously: %s", immediate_url)
        return immediate_url

    # Extract generationId – try every known key name
    generation_id: str | None = (
        start_response.get("generationId")
        or start_response.get("generation_id")
        or start_response.get("id")
        or (start_response.get("generate") or {}).get("generationId")
        or (start_response.get("sdGenerationJob") or {}).get("generationId")
        or (start_response.get("job") or {}).get("id")
    )

    if not generation_id:
        log.error(
            "Could not find generationId in v2 POST response. Full response: %s",
            json.dumps(start_response),
        )
        raise GenerationError(502, f"{ERR_GENERATION_FAILED}: no generationId in response")

    log.info("Leonardo generation started, id=%s", generation_id)

    # Step 2: poll v1 GET until COMPLETE
    poll_url = f"{LEONARDO_API_V1_BASE_URL}{LEONARDO_GENERATIONS_PATH}/{generation_id}"
    for attempt in range(POLL_MAX_ATTEMPTS):
        time.sleep(POLL_INTERVAL_SECONDS)
        poll_response = _make_request("GET", poll_url, api_key)
        log.debug("Poll attempt %d keys: %s", attempt + 1, list(poll_response.keys()))

        # Also check for immediate images inside poll response
        immediate_url = _extract_image_url(poll_response)
        if immediate_url:
            return immediate_url

        generation = poll_response.get("generations_by_pk") or {}
        status = generation.get("status", "")
        generated_images: list = generation.get("generated_images") or []

        log.info("Poll attempt %d: status=%s images=%d", attempt + 1, status, len(generated_images))

        if status == "FAILED":
            raise GenerationError(502, ERR_GENERATION_FAILED)

        if status == "COMPLETE" and generated_images:
            image_url: str = generated_images[0].get("url", "")
            if image_url:
                return image_url
            raise GenerationError(502, ERR_GENERATION_FAILED)

    raise GenerationError(504, ERR_GENERATION_TIMEOUT)
