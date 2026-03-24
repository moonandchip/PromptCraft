from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope used by all endpoints."""
    data: T | None = None
    error: str | None = None
    message: str | None = None
