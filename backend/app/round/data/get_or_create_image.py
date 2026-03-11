import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from .entities import RoundImage

_DIFFICULTY_TO_LEVEL: dict[str, int] = {"easy": 1, "medium": 3, "hard": 5}


def get_or_create_image(session: Session, reference_image: str, difficulty: str) -> str:
    """Returns an image ID for the reference image, creating the image if needed.

    Args:
        session: The SQLAlchemy session used for data access.
        reference_image: The reference image filename for the selected round.
        difficulty: The textual difficulty for the selected round.

    Returns:
        The ID of an existing or newly created image row.

    Raises:
        Exception: Propagates database errors raised by the session.
    """
    existing_image_id = session.execute(
        select(RoundImage.id).where(RoundImage.image_url.like(f"%{reference_image}%")).limit(1)
    ).scalar_one_or_none()
    if existing_image_id is not None:
        return str(existing_image_id)

    new_image = RoundImage(
        id=str(uuid.uuid4()),
        image_url=reference_image,
        difficulty_level=_DIFFICULTY_TO_LEVEL.get(difficulty, 3),
        is_active=True,
    )
    session.add(new_image)
    session.flush()
    return str(new_image.id)
