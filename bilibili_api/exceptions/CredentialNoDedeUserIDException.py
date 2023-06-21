"""
bilibili_api.exceptions.CredentialNoDedeUserID

Credential 类未提供 sessdata 时的异常。
"""

from .ApiException import ApiException


class CredentialNoDedeUserIDException(ApiException):
    """
    Credential 类未提供 DedeUserID 时的异常。
    """

    def __init__(self):
        super().__init__()
        self.msg = "Credential 类未提供 DedeUserID 或者为空。"
