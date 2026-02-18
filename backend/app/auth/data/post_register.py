from ..constants import AUTH_API_REGISTER_PATH, KEY_EMAIL, KEY_NAME, KEY_PASSWORD
from .request_auth_service import request_auth_service


def post_register(
    email: str,
    password: str,
    name: str | None,
    base_url: str,
    timeout_seconds: float,
) -> dict:
    """Call the auth service register endpoint."""
    return request_auth_service(
        method="POST",
        path=AUTH_API_REGISTER_PATH,
        body={KEY_EMAIL: email, KEY_PASSWORD: password, KEY_NAME: name},
        base_url=base_url,
        timeout_seconds=timeout_seconds,
    )
