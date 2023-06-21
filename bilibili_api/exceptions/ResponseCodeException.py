"""
bilibili_api.exceptions.ResponseCodeException

API 返回 code 错误。
"""

from .ApiException import ApiException


class ResponseCodeException(ApiException):
    """
    API 返回 code 错误。
    """

    def __init__(self, code: int, msg: str, raw: dict = None):
        """

        Args:
            code (int):             错误代码。

            msg (str):              错误信息。
            
            raw (dict, optional):   原始响应数据. Defaults to None.
        """
        super().__init__(msg)
        self.msg = msg
        self.code = code
        self.raw = raw

    def __str__(self):
        return f"接口返回错误代码：{self.code}，信息：{self.msg}。\n{self.raw}"
