import logging
import os
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth import router as auth_router
from app.challenge import router as challenge_router
from app.db import dispose_engine
from app.exceptions import AppException
from app.response import ApiResponse
from app.stats import router as stats_router
from app.round import router as round_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def _warm_clip_model() -> None:
    try:
        from app.round.service.clip_scoring import _get_model_and_processor
        _get_model_and_processor()
    except Exception:
        logger.exception("CLIP warmup failed; scoring will lazy-load on first request")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm CLIP in a background thread so startup isn't blocked by the
    # ~600MB download on first run. Opt out in dev via CLIP_SKIP_WARMUP=1.
    if os.environ.get("CLIP_SKIP_WARMUP", "").strip() not in ("1", "true", "True"):
        threading.Thread(target=_warm_clip_model, name="clip-warmup", daemon=True).start()
    yield
    dispose_engine()


app = FastAPI(title="PromptCraft API", lifespan=lifespan)


def _allowed_origins() -> list[str]:
    """Returns the list of explicit allowed CORS origins.

    Set `CORS_ALLOWED_ORIGINS` to a comma-separated list (e.g.
    "https://promptcrafts.net,https://www.promptcrafts.net"). When unset,
    falls back to local development defaults.
    """
    raw = os.environ.get("CORS_ALLOWED_ORIGINS", "").strip()
    if not raw:
        return ["http://localhost:5173"]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def _allowed_origin_regex() -> str | None:
    """Optional regex pattern that's matched in addition to the explicit list,
    useful for wildcard subdomains (e.g. "^https://([a-z0-9-]+\\.)?promptcrafts\\.net$").
    """
    raw = os.environ.get("CORS_ALLOWED_ORIGIN_REGEX", "").strip()
    return raw or None


app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_origin_regex=_allowed_origin_regex(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(stats_router)
app.include_router(round_router)
app.include_router(challenge_router)


@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    body = ApiResponse(data=None, error=exc.error.value, message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


@app.get("/health")
def health() -> ApiResponse:
    return ApiResponse(data={"status": "ok"})
