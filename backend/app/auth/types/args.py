from dataclasses import dataclass


@dataclass(frozen=True)
class LoginArgs:
    email: str
    password: str


@dataclass(frozen=True)
class RegisterArgs:
    email: str
    password: str
    name: str | None = None
