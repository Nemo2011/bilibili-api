"""
bilibili_api.exceptions.ResponseException

API 响应异常
"""

from .ApiException import ApiException


class ResponseException(ApiException):
    def __init__(self, msg: str):
        self.msg = msg
