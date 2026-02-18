import json
from urllib import error, request

from ..constants import (
    BEARER_SCHEME,
    CONTENT_TYPE_JSON,
    EMPTY_JSON_OBJECT,
    ENCODING_UTF8,
    ERR_AUTH_SERVICE_ERROR,
    ERR_AUTH_SERVICE_UNAVAILABLE,
    ERR_INVALID_AUTH_SERVICE_RESPONSE,
    HEADER_AUTHORIZATION,
    HEADER_CONTENT_TYPE,
    KEY_DETAIL,
    KEY_ERROR,
)
from ..service.errors import AuthServiceError


def request_auth_service(
    method: str,
    path: str,
    base_url: str,
    timeout_seconds: float,
    body: dict | None = None,
    bearer_token: str | None = None,
) -> dict:
    """Send an HTTP request to the auth service and return a JSON object response."""
    headers = {HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON}
    if bearer_token:
        headers[HEADER_AUTHORIZATION] = f"{BEARER_SCHEME.capitalize()} {bearer_token}"

    data = None
    if body is not None:
        data = json.dumps(body).encode(ENCODING_UTF8)

    req = request.Request(
        url=f"{base_url}{path}",
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            raw = response.read().decode(ENCODING_UTF8) or EMPTY_JSON_OBJECT
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                raise AuthServiceError(502, ERR_INVALID_AUTH_SERVICE_RESPONSE)
            return parsed
    except error.HTTPError as exc:
        detail = ERR_AUTH_SERVICE_ERROR
        try:
            payload = json.loads(exc.read().decode(ENCODING_UTF8))
            if isinstance(payload, dict):
                detail = str(payload.get(KEY_ERROR) or payload.get(KEY_DETAIL) or detail)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        raise AuthServiceError(exc.code, detail) from exc
    except error.URLError as exc:
        raise AuthServiceError(503, ERR_AUTH_SERVICE_UNAVAILABLE) from exc
