from sqlalchemy.orm import Session

from app.stats.data.entities import Round


def save_round_start(session: Session, user_id: str, round_id: str, target_image_url: str) -> None:
    """Persists a newly started round for a user.

    Args:
        session: The SQLAlchemy session used for data access.
        user_id: The authenticated user ID starting the round.
        round_id: The selected round ID assigned at round start.
        target_image_url: The target reference image URL for the round.

    Raises:
        Exception: Propagates database errors raised during persistence.
    """
    row = Round(
        user_id=user_id,
        score=0.0,
        round_id=round_id,
        target_image_url=target_image_url,
    )
    session.add(row)
    session.commit()
