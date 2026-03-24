from pydantic import BaseModel


class RecentAttempt(BaseModel):
    round_id: str
    attempt_number: int
    prompt: str
    generated_image_url: str
    similarity_score: float = 0.0
    created_at: str | None = None


class StatsResponse(BaseModel):
    total_rounds: int
    total_attempts: int
    average_score: float
    best_score: float
    recent_attempts: list[RecentAttempt] = []
