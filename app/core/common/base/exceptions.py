class BaseAppException(Exception):
    """Base class for app exceptions"""

    def __init__(self, detail: str = "Something went wrong"):
        self.detail = detail

        super().__init__(self.detail)


class UniqueConstraintViolation(BaseAppException):
    """Raised when a unique constraint is violated"""


class ValidationError(BaseAppException):
    """Raised when a validation error occurs"""
