"""
bilibili_api.exceptions.LoginError

登录错误。
"""

from .ApiException import ApiException


class LoginError(ApiException):
    """
    参数错误。
    """

    def __init__(self, msg: str):
        """
        Args:
            msg (str):   错误消息。
        """
        super().__init__(msg)
        self.msg = msg
