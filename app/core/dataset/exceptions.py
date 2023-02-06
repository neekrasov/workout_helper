from app.core.common.base.exceptions import BaseAppException


class ParsingSiteNotAvailable(BaseAppException):
    """Raised when the site to be scraped is not responding"""
