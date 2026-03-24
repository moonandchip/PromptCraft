from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.round.types.log_attributes import (
    AttemptLogAttributes,
    PromptLogAttributes,
    RoundImageLogAttributes,
    RoundUserLogAttributes,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RoundUser(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now)
    total_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    role: Mapped[str] = mapped_column(String, nullable=False, default="user")

    @property
    def log_attributes(self) -> RoundUserLogAttributes:
        return RoundUserLogAttributes(user_id=self.id, email=self.email, role=self.role)


class RoundImage(Base):
    __tablename__ = "images"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    @property
    def log_attributes(self) -> RoundImageLogAttributes:
        return RoundImageLogAttributes(
            image_id=self.id, difficulty_level=self.difficulty_level, is_active=self.is_active,
        )


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    image_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    prompt_text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now)

    @property
    def log_attributes(self) -> PromptLogAttributes:
        return PromptLogAttributes(prompt_id=self.id, user_id=self.user_id, image_id=self.image_id)


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    image_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    prompt_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    round_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    generated_image_url: Mapped[str] = mapped_column(String, nullable=False, default="")
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    time_taken: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now)

    @property
    def log_attributes(self) -> AttemptLogAttributes:
        return AttemptLogAttributes(
            attempt_id=self.id,
            user_id=self.user_id,
            round_id=self.round_id,
            attempt_number=self.attempt_number,
            similarity_score=self.similarity_score,
        )
