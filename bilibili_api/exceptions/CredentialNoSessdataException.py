"""
bilibili_api.exceptions.CredentialNoSessdataException

Credential 类未提供 sessdata 时的异常。
"""

from .ApiException import ApiException


class CredentialNoSessdataException(ApiException):
    """
    Credential 类未提供 sessdata 时的异常。
    """

    def __init__(self):
        super().__init__()
        self.msg = "Credential 类未提供 sessdata。"
