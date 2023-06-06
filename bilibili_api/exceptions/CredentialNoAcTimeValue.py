"""
bilibili_api.exceptions.CredentialNoAcTimeValue

Credential 类未提供 ac_time_value 时的异常。
"""

from .ApiException import ApiException


class CredentialNoAcTimeValueException(ApiException):
    """
    Credential 类未提供 ac_time_value 时的异常。
    """

    def __init__(self):
        super().__init__()
        self.msg = "Credential 类未提供 ac_time_value。"
