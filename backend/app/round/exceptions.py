from app.exceptions import AppException, BaseErrorCodeEnum


class RoundError(BaseErrorCodeEnum):
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    NOT_FOUND = "ROUND_NOT_FOUND"
    GENERATION_FAILED = "ROUND_GENERATION_FAILED"
    GENERATION_TIMEOUT = "ROUND_GENERATION_TIMEOUT"
    NO_API_KEY = "ROUND_NO_API_KEY"
    SAVE_FAILED = "ROUND_SAVE_FAILED"


class SubmitRoundException(AppException):
    def __init__(self, error: RoundError = RoundError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            RoundError.NOT_FOUND: 404,
            RoundError.GENERATION_FAILED: 502,
            RoundError.GENERATION_TIMEOUT: 504,
            RoundError.NO_API_KEY: 500,
            RoundError.SAVE_FAILED: 500,
        }
        super().__init__(error, status_map.get(error, 500), message)


class StartRoundException(AppException):
    def __init__(self, error: RoundError = RoundError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            RoundError.NOT_FOUND: 404,
            RoundError.SAVE_FAILED: 500,
        }
        super().__init__(error, status_map.get(error, 500), message)


class GetRoundAttemptsException(AppException):
    def __init__(self, error: RoundError = RoundError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status = 404 if error == RoundError.NOT_FOUND else 500
        super().__init__(error, status, message)


class GetRoundHistoryException(AppException):
    def __init__(self, error: RoundError = RoundError.UNKNOWN_ERROR, message: str | None = None) -> None:
        super().__init__(error, 500, message)
