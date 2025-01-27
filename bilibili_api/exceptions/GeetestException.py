"""
bilibili_api.exceptions.GeetestException

极验相关错误
"""

from .ApiException import ApiException


class GeetestException(ApiException):
    """
    未找到验证码服务器
    """

    def __init__(self, msg: str = ""):
        super().__init__()
        self.msg = "未找到验证码服务器，请创建服务器。"
