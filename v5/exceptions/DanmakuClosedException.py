"""
bilibili_api.exceptions.DanmakuClosedException

视频弹幕被关闭错误
"""

from .ApiException import ApiException


class DanmakuClosedException(ApiException):
    def __init__(self):
        self.msg = "视频弹幕已关闭"