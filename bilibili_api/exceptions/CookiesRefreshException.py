"""
bilibili_api.exceptions.CookiesRefreshException

Cookies 刷新错误。
"""

from .ApiException import ApiException


class CookiesRefreshException(ApiException):
    """
    Cookies 刷新错误。
    """

    def __init__(self, msg: str = "Cookies 刷新错误。"):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg
