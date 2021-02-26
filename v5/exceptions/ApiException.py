"""
bilibili_api.exceptions.ApiException

API 异常基类
"""


class ApiException(Exception):
    """
    API 基类异常
    """
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
