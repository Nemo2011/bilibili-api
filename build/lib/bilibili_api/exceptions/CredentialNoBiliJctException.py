"""
bilibili_api.exceptions.CredentialNoBiliJctException

Credential 类未提供 bili_jct 时的异常。
"""

from .ApiException import ApiException


class CredentialNoBiliJctException(ApiException):
    """
    Credential 类未提供 bili_jct 时的异常。
    """

    def __init__(self):
        super().__init__()
        self.msg = "Credential 类未提供 bili_jct。"
