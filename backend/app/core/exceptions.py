class AppException(Exception):
    """Base exception"""

    status_code = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppException):
    """Resource does not exist"""

    status_code = 404

    pass


class AccessDeniedError(AppException):
    """User does not have permission"""

    status_code = 403

    pass


class ConflictError(AppException):
    """Duplicate entity or invalid state transition"""

    status_code = 409

    pass


class BadRequest(AppException):
    """Request payload or requested operation is invalid."""

    status_code = 400

    pass


class InternalServerError(AppException):
    """An application operation failed unexpectedly."""

    pass
