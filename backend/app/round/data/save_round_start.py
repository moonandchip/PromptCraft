from sqlalchemy.orm import Session

from app.stats.data.entities import Round


def save_round_start(session: Session, user_id: str, round_id: str, target_image_url: str) -> None:
    """Stages a new `rounds` row for the user. Caller owns the transaction
    (commit/rollback); this function only adds and flushes.
    """
    row = Round(
        user_id=user_id,
        score=0.0,
        round_id=round_id,
        target_image_url=target_image_url,
    )
    session.add(row)
    session.flush()
