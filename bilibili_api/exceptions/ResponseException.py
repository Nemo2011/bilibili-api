"""
bilibili_api.exceptions.ResponseException

API 响应异常。
"""

from .ApiException import ApiException


class ResponseException(ApiException):
    """
    API 响应异常。
    """
    def __init__(self, msg: str):
        """

        Args:
            msg (str): 错误消息。
        """
        super.__call__(msg)
        self.msg = msg
