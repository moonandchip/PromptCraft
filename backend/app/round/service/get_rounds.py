from ..constants import ROUNDS
from ..models import RoundInfo


def get_rounds() -> list[RoundInfo]:
    """Builds the list of all available practice rounds.

    Args:
        None.

    Returns:
        A list of round response models for all configured rounds.

    Raises:
        Exception: Propagates model validation errors if round config is invalid.
    """
    return [RoundInfo(**round_info) for round_info in ROUNDS]
