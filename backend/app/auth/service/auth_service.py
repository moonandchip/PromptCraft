from ..models import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from .build_auth_service_config import build_auth_service_config
from .login import login
from .register_user import register_user
from .resolve_user_from_token import resolve_user_from_token
from .types import AuthServiceConfig


class AuthService:
    def __init__(self, base_url: str | None = None, timeout_seconds: float = 10.0) -> None:
        """Create an auth service facade with resolved runtime configuration."""
        self.config: AuthServiceConfig = build_auth_service_config(
            base_url=base_url,
            timeout_seconds=timeout_seconds,
        )

    def login(self, payload: LoginRequest) -> TokenResponse:
        """Proxy login to the layered service function."""
        return login(payload=payload, config=self.config)

    def register_user(self, payload: RegisterRequest) -> UserResponse:
        """Proxy register to the layered service function."""
        return register_user(payload=payload, config=self.config)

    def resolve_user_from_token(self, token: str) -> UserResponse:
        """Proxy token resolution to the layered service function."""
        return resolve_user_from_token(token=token, config=self.config)
