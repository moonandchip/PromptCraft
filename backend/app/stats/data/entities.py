from dataclasses import dataclass

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


@dataclass(frozen=True)
class RoundLogAttributes:
    round_id: int
    user_id: str
    score: float


class Round(Base):
    __tablename__ = "rounds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)

    @property
    def log_attributes(self) -> RoundLogAttributes:
        return RoundLogAttributes(round_id=self.id, user_id=self.user_id, score=self.score)
