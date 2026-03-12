from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Round(Base):
    __tablename__ = "rounds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
