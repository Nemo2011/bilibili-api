"""
bilibili_api.exceptions.ArgsException

参数错误
"""

from .ApiException import ApiException


class ArgsException(ApiException):
    def __init__(self, msg: str):
        self.msg = msg
