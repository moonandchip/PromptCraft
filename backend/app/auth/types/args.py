from dataclasses import dataclass


@dataclass
class LoginArgs:
    email: str
    password: str


@dataclass
class RegisterArgs:
    email: str
    password: str
    name: str | None = None
