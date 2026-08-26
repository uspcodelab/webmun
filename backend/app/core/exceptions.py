class AppException(Exception):
    """Base exception"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppException):
    """Resource does not exist"""

    pass


class AccessDeniedError(AppException):
    """User does not have permission"""

    pass


class ConflictError(AppException):
    """Duplicate entity or invalid state transition"""

    pass
