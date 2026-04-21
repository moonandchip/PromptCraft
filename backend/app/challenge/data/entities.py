from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db import Base
from app.challenge.types.log_attributes import ChallengeLogAttributes


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    period_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    round_id: Mapped[str] = mapped_column(String, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    @property
    def log_attributes(self) -> ChallengeLogAttributes:
        return ChallengeLogAttributes(
            challenge_id=str(self.id),
            period_type=self.period_type,
            round_id=self.round_id,
        )
