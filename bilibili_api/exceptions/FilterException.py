"""
bilibili_api.exceptions.FilterException

过滤器执行错误。
"""

from .ApiException import ApiException


class FilterException(ApiException):
    """
    过滤器执行错误。
    """

    def __init__(self, filter_pos: str, filter_name: str):
        super().__init__()
        self.msg = {"pre": "前置", "post": "后置"}[filter_pos] + "过滤器 " + filter_name + " 执行失败。"
