from ...common.exceptions import BaseAppException


class InvalidTokenException(BaseAppException):
    """Invalid token exception."""


class InvalidCredentialsException(BaseAppException):
    """Invalid credentials exception."""


class SessionNotFoundException(BaseAppException):
    """Session not found exception."""
