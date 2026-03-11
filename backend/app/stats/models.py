from pydantic import BaseModel


class StatsResponse(BaseModel):
    rounds_played: int
    average_score: float
    best_score: float
