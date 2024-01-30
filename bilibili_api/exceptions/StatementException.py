"""
bilibili_api.exceptions.StatementException

条件异常。
"""

from .ApiException import ApiException


class StatementException(ApiException):
    """
    条件异常。
    """

    def __init__(self, msg: str):
        """

        Args:
            msg (str): 错误消息。
        """
        super().__init__(msg)
        self.msg = msg
