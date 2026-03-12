"""Round module that handles practice round lifecycle and AI image generation.

Layer responsibilities:
- transport: FastAPI-facing endpoints.
- service: business logic (Leonardo API image generation, CLIP scoring).
- data: database access (persist prompts and attempts).

Endpoints:
  GET  /round/rounds   - list all available practice rounds.
  POST /round/start    - start a round for an authenticated user.
  POST /round/submit   - submit a prompt, generate an image, persist it, and return it.
"""

from .transport.router import router

__all__ = ["router"]
