from dataclasses import dataclass


@dataclass(frozen=True)
class AuthServiceConfig:
    base_url: str
    timeout_seconds: float
