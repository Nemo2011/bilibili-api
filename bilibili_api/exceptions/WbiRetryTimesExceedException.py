"""
bilibili_api.exceptions.WbiRetryTimesExceedException

Wbi 重试达到最大次数
"""

from .ApiException import ApiException


class WbiRetryTimesExceedException(ApiException):
    """
    Wbi 重试达到最大次数
    """

    def __init__(self):
        super().__init__()
        self.msg = "Wbi 重试达到最大次数"
