"""
bilibili_api.exceptions.CredentialNoBuvid3Exception

Credential 类未提供 buvid3 时的异常。
"""

from .ApiException import ApiException


class CredentialNoBuvid3Exception(ApiException):
    """
    Credential 类未提供 bili_jct 时的异常。
    """

    def __init__(self):
        super().__init__()
        self.msg = "Credential 类未提供 buvid3。"
