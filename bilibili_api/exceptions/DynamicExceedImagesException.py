"""
bilibili_api.exceptions.DanmakuClosedException

动态上传图片数量超过限制
"""

from .ApiException import ApiException


class DynamicExceedImagesException(ApiException):
    """
    动态上传图片数量超过限制
    """

    def __init__(self):
        super().__init__()
        self.msg = "最多上传 9 张图片"
