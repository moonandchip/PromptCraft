from ..models import RoundInfo
from ..service import get_rounds


def get_rounds_endpoint() -> list[RoundInfo]:
    """Handles returning all available practice rounds.

    Args:
        None.

    Returns:
        A list of available rounds.

    Raises:
        Exception: Propagates service-layer errors.
    """
    return get_rounds()
