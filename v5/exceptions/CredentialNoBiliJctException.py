"""
bilibili_api.exceptions.CredentialNoBiliJctException

Credential 类未提供 sessdata 时的异常
"""

from .ApiException import ApiException


class CredentialNoBiliJctException(ApiException):
    def __init__(self):
        self.msg = "Credential 类未提供 bili_jct"
