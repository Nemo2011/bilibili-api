"""
bilibili_api.exceptions.GeetestUndoneException

验证码未完成
"""

from .ApiException import ApiException


class GeetestUndoneException(ApiException):
    """
    验证码未完成
    """

    def __init__(self):
        super().__init__()
        self.msg = "验证码未完成"
