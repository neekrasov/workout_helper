from ..base.exceptions import BaseAppException


class CommandNotFoundException(BaseAppException):
    """Raised when an event is not found in the event store."""
