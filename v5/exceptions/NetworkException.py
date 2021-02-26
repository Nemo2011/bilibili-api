"""
bilibili_api.exceptions.NetworkException

请求网络错误
"""

from .ApiException import ApiException


class NetworkException(ApiException):
    def __init__(self, status: int, msg: str):
        self.status = status
        self.msg = f"网络错误，状态码：{status} - {msg}"

    def __str__(self):
        return self.msg
