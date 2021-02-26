"""
bilibili_api.exceptions.VideoNoIdException

Video 类未提供任何有效 ID
"""

from .ApiException import ApiException


class VideoNoIdException(ApiException):
    def __init__(self):
        self.msg = "未提供有效视频ID（BV 号或 AV 号）"
