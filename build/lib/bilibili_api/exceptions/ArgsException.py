"""
bilibili_api.exceptions.ArgsException

参数错误。
"""

from .ApiException import ApiException


class ArgsException(ApiException):
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
