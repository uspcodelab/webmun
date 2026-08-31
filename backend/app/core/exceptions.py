class AppException(Exception):
    """Base exception for expected application failures."""

    status_code = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class BadRequest(AppException):
    status_code = 400


class AccessDeniedError(AppException):
    status_code = 403


class NotFoundError(AppException):
    status_code = 404


class ConflictError(AppException):
    status_code = 409


class InternalServerError(AppException):
    pass
