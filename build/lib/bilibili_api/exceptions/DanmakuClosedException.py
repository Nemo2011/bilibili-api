"""
bilibili_api.exceptions.DanmakuClosedException

视频弹幕被关闭错误。
"""

from .ApiException import ApiException


class DanmakuClosedException(ApiException):
    """
    视频弹幕被关闭错误。
    """

    def __init__(self):
        super().__init__()
        self.msg = "视频弹幕已关闭。"
