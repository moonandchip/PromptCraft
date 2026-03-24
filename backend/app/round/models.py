from pydantic import BaseModel, Field


class RoundSubmitRequest(BaseModel):
    round_id: str = Field(min_length=1, max_length=100)
    user_prompt: str = Field(min_length=1, max_length=2000)


class RoundSubmitResponse(BaseModel):
    generated_image_url: str
    similarity_score: float = 0.0


class RoundStartResponse(BaseModel):
    round_id: str
    target_image_url: str


class RoundInfo(BaseModel):
    id: str
    title: str
    difficulty: str
    reference_image: str


class RoundAttemptResponse(BaseModel):
    attempt_number: int = Field(ge=1)
    prompt: str
    generated_image_url: str
    similarity_score: float = 0.0


