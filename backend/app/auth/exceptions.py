from app.exceptions import AppException, BaseErrorCodeEnum


class AuthError(BaseErrorCodeEnum):
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    SERVICE_UNAVAILABLE = "AUTH_SERVICE_UNAVAILABLE"
    INVALID_TOKEN = "AUTH_INVALID_TOKEN"


class LoginException(AppException):
    def __init__(self, error: AuthError = AuthError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            AuthError.INVALID_CREDENTIALS: 401,
            AuthError.SERVICE_UNAVAILABLE: 503,
        }
        super().__init__(error, status_map.get(error, 500), message)


class RegisterException(AppException):
    def __init__(self, error: AuthError = AuthError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            AuthError.INVALID_CREDENTIALS: 409,
            AuthError.SERVICE_UNAVAILABLE: 503,
        }
        super().__init__(error, status_map.get(error, 500), message)


class ResolveTokenException(AppException):
    def __init__(self, error: AuthError = AuthError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            AuthError.INVALID_TOKEN: 401,
            AuthError.SERVICE_UNAVAILABLE: 503,
        }
        super().__init__(error, status_map.get(error, 500), message)
