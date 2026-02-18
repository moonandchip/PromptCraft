from ..constants import AUTH_API_INTERNAL_ME_PATH
from .request_auth_service import request_auth_service


def get_internal_me(token: str, base_url: str, timeout_seconds: float) -> dict:
    """Call the auth service internal identity endpoint using a bearer token."""
    return request_auth_service(
        method="GET",
        path=AUTH_API_INTERNAL_ME_PATH,
        bearer_token=token,
        base_url=base_url,
        timeout_seconds=timeout_seconds,
    )
