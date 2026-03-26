from app.exceptions import AppException, BaseErrorCodeEnum


class StatsError(BaseErrorCodeEnum):
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class GetStatsException(AppException):
    def __init__(self, error: StatsError = StatsError.UNKNOWN_ERROR, message: str | None = None) -> None:
        super().__init__(error, 500, message)
