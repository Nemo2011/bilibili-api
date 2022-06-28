"""
bilibili_api.exceptions.ApiException

API 异常基类。
"""


class ApiException(Exception):
    """
    API 基类异常。
    """

    def __init__(self, msg: str = "出现了错误，但是未说明具体原因。"):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg
