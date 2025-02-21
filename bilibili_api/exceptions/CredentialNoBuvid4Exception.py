"""
bilibili_api.exceptions.CredentialNoBuvid4Exception

Credential 类未提供 buvid4 时的异常。
"""

from .ApiException import ApiException


class CredentialNoBuvid4Exception(ApiException):
    """
    Credential 类未提供 buvid4 时的异常。
    """

    def __init__(self):
        super().__init__()
        self.msg = "Credential 类未提供 buvid4 或者为空。"
