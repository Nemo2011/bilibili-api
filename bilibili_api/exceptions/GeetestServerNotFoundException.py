"""
bilibili_api.exceptions.GeetestServerNotFoundException

未找到验证码服务器
"""

from .ApiException import ApiException


class GeetestServerNotFoundException(ApiException):
    """
    未找到验证码服务器
    """

    def __init__(self):
        super().__init__()
        self.msg = "未找到验证码服务器，请创建服务器。"
