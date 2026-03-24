from app.exceptions import AppException, BaseErrorCodeEnum


class RoundError(BaseErrorCodeEnum):
    UNKNOWN_ERROR = "ROUND_UNKNOWN_ERROR"
    NOT_FOUND = "ROUND_NOT_FOUND"
    GENERATION_FAILED = "ROUND_GENERATION_FAILED"
    GENERATION_TIMEOUT = "ROUND_GENERATION_TIMEOUT"
    NO_API_KEY = "ROUND_NO_API_KEY"
    SAVE_FAILED = "ROUND_SAVE_FAILED"


class SubmitRoundException(AppException):
    """Raised when a round submission fails."""
    pass


class StartRoundException(AppException):
    """Raised when starting a round fails."""
    pass


class GetRoundAttemptsException(AppException):
    """Raised when retrieving round attempts fails."""
    pass
