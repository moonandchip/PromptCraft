from typing import TypedDict


class AttemptLogAttributes(TypedDict):
    attempt_id: str
    user_id: str
    round_id: str
    attempt_number: int
    similarity_score: float


class RoundUserLogAttributes(TypedDict):
    user_id: str
    email: str
    role: str


class PromptLogAttributes(TypedDict):
    prompt_id: str
    user_id: str
    image_id: str


class RoundImageLogAttributes(TypedDict):
    image_id: str
    difficulty_level: int
    is_active: bool
