"""
bilibili_api.exceptions.LiveException

"""

from .ApiException import ApiException


class LiveException(ApiException):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg
