from app.exceptions import AppException, BaseErrorCodeEnum


class AuthError(BaseErrorCodeEnum):
    UNKNOWN_ERROR = "AUTH_UNKNOWN_ERROR"
    INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    SERVICE_UNAVAILABLE = "AUTH_SERVICE_UNAVAILABLE"
    INVALID_TOKEN = "AUTH_INVALID_TOKEN"


class LoginException(AppException):
    """Raised when user login fails."""
    pass


class RegisterException(AppException):
    """Raised when user registration fails."""
    pass


class ResolveTokenException(AppException):
    """Raised when token resolution fails."""
    pass
