"""
bilibili_api.exceptions.ApiContentTypeException

API 返回类型异常
"""

from .ApiException import ApiException


class ApiContentTypeException(ApiException):
    def __init__(self, content_type: str):
        self.msg = f"接口返回类型错误：{content_type}，期望返回：application/json。"
