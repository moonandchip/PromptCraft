from pydantic import BaseModel, Field


class ChallengeStateResponse(BaseModel):
    challenge_id: str
    period_type: str
    period_end: str
    round_id: str
    title: str
    difficulty: str
    target_image_url: str
    max_attempts: int
    attempts_used: int
    best_score: float = 0.0


class ChallengeSubmitRequest(BaseModel):
    user_prompt: str = Field(min_length=1, max_length=2000)


class ChallengeSubmitResponse(BaseModel):
    generated_image_url: str
    similarity_score: float = 0.0
    attempts_used: int
    attempts_remaining: int
    best_score: float = 0.0


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
