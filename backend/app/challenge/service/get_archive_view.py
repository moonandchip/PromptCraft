import logging

from sqlalchemy.orm import Session

from app.round.constants import ROUNDS

from ..constants import ARCHIVE_DEFAULT_LIMIT, CHANNEL, GET_ARCHIVE_FEATURE
from ..data import get_user_archive
from ..models import ArchiveEntry, ArchiveResponse
from ..types.args import GetArchiveArgs

logger = logging.getLogger(__name__)
_ROUNDS_BY_ID = {r["id"]: r for r in ROUNDS}


def get_archive_view(session: Session, args: GetArchiveArgs) -> ArchiveResponse:
    limit = args.limit or ARCHIVE_DEFAULT_LIMIT
    rows = get_user_archive(session=session, user_id=args.user_id, limit=limit)

    entries: list[ArchiveEntry] = []
    for row in rows:
        round_info = _ROUNDS_BY_ID.get(row["round_id"])
        if round_info is None:
            logger.warning(
                "Archive references unknown round; skipping",
                extra={"channel": CHANNEL, "feature": GET_ARCHIVE_FEATURE, "round_id": row["round_id"]},
            )
            continue
        entries.append(ArchiveEntry(
            challenge_id=row["challenge_id"],
            period_start=row["period_start"].isoformat(),
            period_end=row["period_end"].isoformat(),
            round_id=row["round_id"],
            title=round_info["title"],
            difficulty=round_info["difficulty"],
            target_image_url=f"/static/{round_info['reference_image']}",
            max_attempts=row["max_attempts"],
            attempts_used=row["attempts_used"],
            best_score=row["best_score"],
        ))

    return ArchiveResponse(entries=entries)
