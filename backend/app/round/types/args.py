from dataclasses import dataclass


@dataclass(frozen=True)
class SubmitRoundArgs:
    session_factory: object  # sessionmaker or Session, kept generic for DI
    user_email: str
    round_id: str
    user_prompt: str


@dataclass(frozen=True)
class StartRoundArgs:
    session_factory: object
    user_id: str
