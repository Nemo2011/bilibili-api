"""
bilibili_api.exceptions.InitialStateException

get_initial_state 错误。
"""

from .ApiException import ApiException


class InitialStateException(ApiException):
    """
    获取初始化信息错误。
    """

    def __init__(self, msg: str):
        """
        Args:
            msg (str):   错误消息。
        """
        super().__init__(msg)
        self.msg = msg
