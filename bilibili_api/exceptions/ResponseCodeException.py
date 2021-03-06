"""
bilibili_api.exceptions.ResponseCodeException

API 返回 code 错误
"""

from .ApiException import ApiException


class ResponseCodeException(ApiException):
    def __init__(self, code: int, msg: str, raw: dict = None):
        self.msg = msg
        self.code = code
        self.raw = raw

    def __str__(self):
        return f"接口返回错误代码：{self.code}，信息：{self.msg}"
