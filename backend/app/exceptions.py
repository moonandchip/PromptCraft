from enum import Enum


class BaseErrorCodeEnum(str, Enum):
    """Parent of all domain error enums. Inheriting from str
    makes values JSON-serialisable without extra conversion."""
    pass


class AppException(Exception):
    """Base for all typed application exceptions."""

    def __init__(self, error: BaseErrorCodeEnum, status_code: int = 500, message: str | None = None) -> None:
        self.error = error
        self.status_code = status_code
        self.message = message or str(error.value)
        super().__init__(self.message)
