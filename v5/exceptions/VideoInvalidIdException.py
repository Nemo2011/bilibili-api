"""
bilibili_api.exceptions.VideoInvalidIdException

Video 类 ID 错误
"""

from .ApiException import ApiException


class VideoInvalidIdException(ApiException):
    def __init__(self, msg: str):
        self.msg = msg
