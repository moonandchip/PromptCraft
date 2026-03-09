from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.db import dispose_engine
from app.stats import router as stats_router

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

@app.on_event("shutdown")
def on_shutdown() -> None:
    dispose_engine()


@app.get("/health")
def health():
    return {"status": "ok"}
