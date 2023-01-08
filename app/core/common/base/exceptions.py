class BaseAppException(Exception):
    """Base class for app exceptions"""


class UniqueConstraintViolation(BaseAppException):
    """Raised when a unique constraint is violated"""
