from app.exceptions import AppException, BaseErrorCodeEnum


class StatsError(BaseErrorCodeEnum):
    UNKNOWN_ERROR = "STATS_UNKNOWN_ERROR"


class GetStatsException(AppException):
    """Raised when retrieving user stats fails."""
    pass
