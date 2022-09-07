"""
bilibili_api.exceptions.VideoUploadException

视频上传错误。
"""

from .ApiException import ApiException


class VideoUploadException(ApiException):
    """
    视频上传错误。
    """

    def __init__(self, msg: str):
        """
        Args:
            msg (str):   错误消息。
        """
        super().__init__(msg)
        self.msg = msg
