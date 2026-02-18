"""Authentication module organized by transport, service, and data layers.

Layer responsibilities:
- transport: FastAPI-facing endpoints and dependency helpers.
- service: business orchestration and response validation.
- data: outbound HTTP calls to the external auth service.

Runtime flow:
1. FastAPI routes in `transport` receive requests.
2. Service functions in `service` execute auth use-cases.
3. Data functions in `data` call the auth service API.
"""

from .router import router

__all__ = ["router"]
