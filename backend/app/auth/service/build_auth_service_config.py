import os

from ..constants import AUTH_SERVICE_URL_ENV_VAR, DEFAULT_AUTH_SERVICE_URL
from .types import AuthServiceConfig


def build_auth_service_config(
    base_url: str | None = None,
    timeout_seconds: float = 10.0,
) -> AuthServiceConfig:
    """Build resolved auth service configuration from args and environment."""
    resolved_base_url = (base_url or os.getenv(AUTH_SERVICE_URL_ENV_VAR, DEFAULT_AUTH_SERVICE_URL)).rstrip("/")
    return AuthServiceConfig(base_url=resolved_base_url, timeout_seconds=timeout_seconds)
