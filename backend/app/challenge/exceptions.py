from app.exceptions import AppException, BaseErrorCodeEnum


class ChallengeError(BaseErrorCodeEnum):
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    NOT_FOUND = "CHALLENGE_NOT_FOUND"
    ATTEMPT_LIMIT_REACHED = "CHALLENGE_ATTEMPT_LIMIT_REACHED"
    GENERATION_FAILED = "CHALLENGE_GENERATION_FAILED"
    GENERATION_TIMEOUT = "CHALLENGE_GENERATION_TIMEOUT"
    SAVE_FAILED = "CHALLENGE_SAVE_FAILED"


class GetCurrentChallengeException(AppException):
    def __init__(self, error: ChallengeError = ChallengeError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {ChallengeError.NOT_FOUND: 404}
        super().__init__(error, status_map.get(error, 500), message)


class SubmitChallengeException(AppException):
    def __init__(self, error: ChallengeError = ChallengeError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            ChallengeError.NOT_FOUND: 404,
            ChallengeError.ATTEMPT_LIMIT_REACHED: 429,
            ChallengeError.GENERATION_FAILED: 502,
            ChallengeError.GENERATION_TIMEOUT: 504,
            ChallengeError.SAVE_FAILED: 500,
        }
        super().__init__(error, status_map.get(error, 500), message)


class GetLeaderboardException(AppException):
    def __init__(self, error: ChallengeError = ChallengeError.UNKNOWN_ERROR, message: str | None = None) -> None:
        super().__init__(error, 500, message)
