from pydantic import BaseModel, Field


class SubmitRequest(BaseModel):
    round_id: str = Field(min_length=1, max_length=100)
    user_prompt: str = Field(min_length=1, max_length=2000)


class SubmitResponse(BaseModel):
    generated_image_url: str
    similarity_score: float = 0.0


class StartRoundResponse(BaseModel):
    round_id: str
    target_image_url: str


class RoundInfo(BaseModel):
    id: str
    title: str
    difficulty: str
    reference_image: str
