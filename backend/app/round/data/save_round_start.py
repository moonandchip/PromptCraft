from sqlalchemy import Float, String, column, insert, table
from sqlalchemy.orm import Session


def save_round_start(session: Session, user_id: str, round_id: str, target_image_url: str) -> None:
    """Persists a newly started round for a user.

    Args:
        session: The SQLAlchemy session used for data access.
        user_id: The authenticated user ID starting the round.
        round_id: The selected round ID assigned at round start.
        target_image_url: The target reference image URL for the round.

    Returns:
        None.

    Raises:
        Exception: Propagates database errors raised during persistence.
    """
    rounds_with_target_columns = table(
        "rounds",
        column("user_id", String),
        column("score", Float),
        column("round_id", String),
        column("target_image_url", String),
    )
    rounds_minimal_columns = table(
        "rounds",
        column("user_id", String),
        column("score", Float),
    )

    try:
        session.execute(
            insert(rounds_with_target_columns).values(
                user_id=user_id,
                score=0.0,
                round_id=round_id,
                target_image_url=target_image_url,
            )
        )
        session.commit()
    except Exception:
        session.rollback()
        session.execute(
            insert(rounds_minimal_columns).values(
                user_id=user_id,
                score=0.0,
            )
        )
        session.commit()
