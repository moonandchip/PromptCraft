from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base


class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, ForeignKey("User.id"))

    target_image_url = Column(String, nullable=False)

    user_prompt = Column(String, nullable=True)

    generated_image_url = Column(String, nullable=True)

    similarity_score = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())