from enum import Enum


class BaseErrorCodeEnum(str, Enum):
    """Base class for domain-specific error code enums."""
    pass


class AppException(Exception):
    """Base application exception carrying a typed error code and HTTP status."""

    def __init__(self, status_code: int, error_code: BaseErrorCodeEnum, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
