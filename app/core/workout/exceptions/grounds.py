from app.core.common.base.exceptions import BaseAppException


class GroundsNotFoundException(BaseAppException):
    "No grounds were found for the given coordinates"


class UserDoesNotLikeGroundException(BaseAppException):
    "User does not like the ground"


class UserAlreadyLikedGroundException(BaseAppException):
    "User already liked the ground"
