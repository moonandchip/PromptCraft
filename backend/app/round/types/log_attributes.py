from dataclasses import dataclass


@dataclass(frozen=True)
class AttemptLogAttributes:
    attempt_id: str
    user_id: str
    round_id: str
    attempt_number: int
    similarity_score: float


@dataclass(frozen=True)
class RoundUserLogAttributes:
    user_id: str
    email: str
    role: str


@dataclass(frozen=True)
class PromptLogAttributes:
    prompt_id: str
    user_id: str
    image_id: str


@dataclass(frozen=True)
class RoundImageLogAttributes:
    image_id: str
    difficulty_level: int
    is_active: bool
