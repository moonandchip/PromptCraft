from datetime import datetime, timezone
from typing import TypedDict
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db import Base


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RoundLogAttributes(TypedDict):
    round_id: str
    user_id: str
    score: float


class Round(Base):
    __tablename__ = "rounds"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(nullable=False)
    round_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    target_image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    @property
    def log_attributes(self) -> RoundLogAttributes:
        return RoundLogAttributes(round_id=self.id, user_id=self.user_id, score=self.score)
