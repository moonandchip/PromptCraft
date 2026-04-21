from sqlalchemy.orm import Session

from ..data import get_leaderboard
from ..models import LeaderboardEntry, LeaderboardResponse
from ..types.args import GetLeaderboardArgs
from .get_or_create_current_challenge import get_or_create_current_challenge


def get_leaderboard_view(session: Session, args: GetLeaderboardArgs) -> LeaderboardResponse:
    challenge = get_or_create_current_challenge(session=session)
    rows = get_leaderboard(session=session, challenge_id=str(challenge.id), limit=args.limit)

    entries = [
        LeaderboardEntry(
            rank=index + 1,
            user_id=user_id,
            display_name=display_name,
            best_score=best_score,
            attempts_used=attempts_used,
        )
        for index, (user_id, display_name, best_score, attempts_used) in enumerate(rows)
    ]
    return LeaderboardResponse(
        challenge_id=str(challenge.id),
        period_end=challenge.period_end.isoformat(),
        entries=entries,
    )
