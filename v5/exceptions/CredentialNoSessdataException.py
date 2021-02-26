"""
bilibili_api.exceptions.CredentialNoSessdataException

Credential 类未提供 sessdata 时的异常
"""

from .ApiException import ApiException


class CredentialNoSessdataException(ApiException):
    def __init__(self):
        self.msg = "Credential 类未提供 sessdata"