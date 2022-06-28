"""
bilibili_api.utils.Credential

凭据类，用于各种请求操作的验证。
"""
from bilibili_api.exceptions.CredentialNoBuvid3Exception import (
    CredentialNoBuvid3Exception,
)
from ..exceptions import CredentialNoBiliJctException, CredentialNoSessdataException


class Credential:
    """
    凭据类，用于各种请求操作的验证。
    """

    def __init__(self, sessdata: str = None, bili_jct: str = None, buvid3: str = None):
        """
        各字段获取方式查看：https://bili.moyu.moe/#/get-credential.md

        Args:
            sessdata (str, optional):  浏览器 Cookies 中的 SESSDATA 字段值
            bili_jct (str, optional):  浏览器 Cookies 中的 bili_jct 字段值
            buvid3 (str, optional):    浏览器 Cookies 中的 BUVID3 字段值
        """
        self.sessdata = sessdata
        self.bili_jct = bili_jct
        self.buvid3 = buvid3

    def get_cookies(self):
        """
        获取请求 Cookies 字典

        Returns:
            dict: 请求 Cookies 字典
        """
        return {
            "SESSDATA": self.sessdata,
            "buvid3": self.buvid3,
            "bili_jct": self.bili_jct,
        }

    def has_sessdata(self):
        """
        是否提供 sessdata。

        Returns:
            bool。
        """
        return self.sessdata is not None

    def has_bili_jct(self):
        """
        是否提供 bili_jct。

        Returns:
            bool。
        """
        return self.bili_jct is not None

    def has_buvid3(self):
        """
        是否提供 buvid3

        Returns:
            bool.
        """
        return self.buvid3 is not None

    def raise_for_no_sessdata(self):
        """
        没有提供 sessdata 则抛出异常。
        """
        if not self.has_sessdata():
            raise CredentialNoSessdataException()

    def raise_for_no_bili_jct(self):
        """
        没有提供 bili_jct 则抛出异常。
        """
        if not self.has_bili_jct():
            raise CredentialNoBiliJctException()

    def raise_for_no_buvid3(self):
        """
        没有提供 buvid3 时抛出异常。
        """
        if not self.has_buvid3():
            raise CredentialNoBuvid3Exception()
