import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth import router as auth_router
from app.db import dispose_engine
from app.exceptions import AppException
from app.response import ApiResponse
from app.stats import router as stats_router
from app.round import router as round_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(title="PromptCraft API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(stats_router)
app.include_router(round_router)


@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    body = ApiResponse(data=None, error=exc.error_code.value, message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


@app.on_event("shutdown")
def on_shutdown() -> None:
    dispose_engine()


@app.get("/health")
def health() -> ApiResponse:
    return ApiResponse(data={"status": "ok"})
