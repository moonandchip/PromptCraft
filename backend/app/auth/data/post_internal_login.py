from ..constants import AUTH_API_INTERNAL_LOGIN_PATH, KEY_EMAIL, KEY_PASSWORD
from .request_auth_service import request_auth_service


def post_internal_login(
    email: str,
    password: str,
    base_url: str,
    timeout_seconds: float,
) -> dict:
    """Call the auth service internal login endpoint."""
    return request_auth_service(
        method="POST",
        path=AUTH_API_INTERNAL_LOGIN_PATH,
        body={KEY_EMAIL: email, KEY_PASSWORD: password},
        base_url=base_url,
        timeout_seconds=timeout_seconds,
    )
