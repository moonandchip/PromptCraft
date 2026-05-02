from pydantic import BaseModel, Field


class ChallengeStateResponse(BaseModel):
    challenge_id: str
    period_type: str
    period_end: str
    round_id: str
    title: str
    difficulty: str
    target_image_url: str
    target_prompt: str | None = None
    max_attempts: int
    attempts_used: int
    best_score: float = 0.0
    current_streak: int = 0
    longest_streak: int = 0


class ChallengeSubmitRequest(BaseModel):
    user_prompt: str = Field(
        min_length=10,
        max_length=2000,
        description="Describe the scene in at least 10 characters.",
    )


class ChallengeSubmitResponse(BaseModel):
    generated_image_url: str
    similarity_score: float = 0.0
    attempts_used: int
    attempts_remaining: int
    best_score: float = 0.0
    current_streak: int = 0
    longest_streak: int = 0
    feedback: list[str] = []


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    display_name: str
    best_score: float
    attempts_used: int


class LeaderboardResponse(BaseModel):
    challenge_id: str
    period_end: str
    entries: list[LeaderboardEntry]


class ArchiveEntry(BaseModel):
    challenge_id: str
    period_start: str
    period_end: str
    round_id: str
    title: str
    difficulty: str
    target_image_url: str
    max_attempts: int
    attempts_used: int
    best_score: float


class ArchiveResponse(BaseModel):
    entries: list[ArchiveEntry]
