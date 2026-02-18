from ..service.build_auth_service_config import build_auth_service_config
from ..service.types import AuthServiceConfig

_service_config = build_auth_service_config()


def get_auth_service() -> AuthServiceConfig:
    """Provide singleton auth service configuration for dependency injection."""
    return _service_config
