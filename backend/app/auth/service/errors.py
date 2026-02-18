class AuthServiceError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        """Wrap auth-service errors with HTTP semantics."""
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
