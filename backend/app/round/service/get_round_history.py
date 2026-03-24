from sqlalchemy.orm import Session

from ..constants import ROUNDS
from ..data import get_round_history_by_user_id
from ..models import RoundHistoryResponse


_ROUNDS_BY_ID = {r["id"]: r for r in ROUNDS}


def get_round_history(session: Session, user_id: str) -> list[RoundHistoryResponse]:
    rows = get_round_history_by_user_id(session=session, user_id=user_id)
    results = []
    for round_id, best_score, attempt_count in rows:
        round_info = _ROUNDS_BY_ID.get(round_id)
        if round_info is None:
            continue
        results.append(
            RoundHistoryResponse(
                round_id=round_id,
                title=round_info["title"],
                difficulty=round_info["difficulty"],
                target_image_url=f"/static/{round_info['reference_image']}",
                best_score=best_score,
                attempt_count=attempt_count,
            )
        )
    return results
