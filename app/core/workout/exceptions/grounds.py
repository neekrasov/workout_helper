from app.core.common.base.exceptions import BaseAppException


class GroundsNotFoundException(BaseAppException):
    "No grounds were found for the given coordinates"
