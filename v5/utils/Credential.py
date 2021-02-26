"""
bilibili_api.utils.Credential

凭据类，用于各种请求操作的验证
"""

from ..exceptions import CredentialNoBiliJctException, CredentialNoSessdataException


class Credential:
    """
    凭据类，用于各种请求操作的验证
    """
    def __init__(self, sessdata: str = None, bili_jct: str = None):
        """
        :param sessdata: 浏览器 Cookies 中的 SESSDATA 字段值
        :param bili_jct: 浏览器 Cookies 中的 bili_jct 字段值
        """
        self.sessdata = sessdata
        self.bili_jct = bili_jct

    def get_cookies(self):
        """
        获取 Cookies
        """
        return {"SESSDATA": self.sessdata}

    def has_sessdata(self):
        """
        是否提供 sessdata
        """
        return self.sessdata is not None

    def has_bili_jct(self):
        """
        是否提供 bili_jct
        """
        return self.bili_jct is not None

    def check_valid(self):
        """
        检查凭据是否有效
        """
        pass
        # @TODO 检查凭据是否有效

    def raise_for_no_sessdata(self):
        """
        没有提供 sessdata 则抛出异常
        """
        if not self.has_sessdata():
            raise CredentialNoSessdataException()

    def raise_for_no_bili_jct(self):
        """
        没有提供 bili_jct 则抛出异常
        """
        if not self.has_bili_jct():
            raise CredentialNoBiliJctException()