"""
bilibili_api.exceptions.ExClimbWuzhiException

ExClimbWuzhi 失败异常
"""

from .ApiException import ApiException


class ExClimbWuzhiException(ApiException):
    """
    ExClimbWuzhi 失败异常
    """

    def __init__(self, code: int, msg: str):
        super().__init__()
        self.msg = f"ExClimbWuzhi 失败，信息: {code} - {msg}"
