from ..constants import ROUNDS


def get_round_by_id(round_id: str) -> dict | None:
    """Finds a configured round by its ID.

    Args:
        round_id: The round ID to find in static round configuration.

    Returns:
        The round configuration dictionary when found, otherwise None.

    Raises:
        Exception: This function does not raise in normal operation.
    """
    return next((round_info for round_info in ROUNDS if round_info["id"] == round_id), None)
