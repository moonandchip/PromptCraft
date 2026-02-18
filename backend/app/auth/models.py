from pydantic import BaseModel, Field, field_validator

from .constants import BEARER_SCHEME, ERR_INVALID_EMAIL_FORMAT


class RegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=128)
    name: str | None = Field(default=None, min_length=1, max_length=120)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Normalize and minimally validate an email field."""
        normalized = value.strip().lower()
        if "@" not in normalized or "." not in normalized.split("@")[-1]:
            raise ValueError(ERR_INVALID_EMAIL_FORMAT)
        return normalized


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Normalize and minimally validate an email field."""
        normalized = value.strip().lower()
        if "@" not in normalized or "." not in normalized.split("@")[-1]:
            raise ValueError(ERR_INVALID_EMAIL_FORMAT)
        return normalized


class UserResponse(BaseModel):
    id: str
    email: str
    name: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = BEARER_SCHEME
