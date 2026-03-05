from .models import StatsResponse


def _placeholder_for_connection(connection: object) -> str:
    if connection.__class__.__module__.startswith("sqlite3"):
        return "?"
    return "%s"


def get_user_stats(connection: object, user_id: str) -> StatsResponse:
    placeholder = _placeholder_for_connection(connection)
    query = (
        "SELECT COUNT(*) AS rounds_played, "
        "COALESCE(AVG(score), 0) AS average_score, "
        "COALESCE(MAX(score), 0) AS best_score "
        f"FROM rounds WHERE user_id = {placeholder}"
    )

    cursor = connection.cursor()
    try:
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
    finally:
        cursor.close()

    if row is None:
        return StatsResponse(rounds_played=0, average_score=0.0, best_score=0.0)

    rounds_played = int(row[0] or 0)
    average_score = float(row[1] or 0.0)
    best_score = float(row[2] or 0.0)
    return StatsResponse(
        rounds_played=rounds_played,
        average_score=average_score,
        best_score=best_score,
    )
