"""Round module – handles practice round lifecycle and AI image generation.

Layer responsibilities:
- transport: FastAPI-facing endpoints.
- service: business logic (Leonardo API image generation).
- data: (reserved for DB access when a database is added).

Endpoints:
  GET  /round/rounds   – list all available practice rounds.
  POST /round/submit   – submit a prompt and receive a generated image URL.
"""
from .transport.router import router

__all__ = ["router"]
