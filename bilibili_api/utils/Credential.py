"""
bilibili_api.utils.Credential

凭据类，用于各种请求操作的验证。
"""

import json
from ..exceptions import (
    CredentialNoBiliJctException,
    CredentialNoSessdataException,
    CredentialNoBuvid3Exception,
    CredentialNoDedeUserIDException,
)
from .utils import get_api
from .cookie_refresh import check_cookies, refresh_cookies
import httpx
import uuid
from typing import Union

API = get_api("credential")


class Credential:
    """
    凭据类，用于各种请求操作的验证。
    """

    def __init__(
        self,
        sessdata: Union[str, None] = None,
        bili_jct: Union[str, None] = None,
        buvid3: Union[str, None] = None,
        dedeuserid: Union[str, None] = None,
        ac_time_value: Union[str, None] = None,
    ):
        """
        各字段获取方式查看：https://nemo2011.github.io/bilibili-api/#/get-credential.md

        Args:
            sessdata   (str | None, optional): 浏览器 Cookies 中的 SESSDATA 字段值. Defaults to None.
            bili_jct   (str | None, optional): 浏览器 Cookies 中的 bili_jct 字段值. Defaults to None.
            buvid3     (str | None, optional): 浏览器 Cookies 中的 BUVID3 字段值. Defaults to None.
            dedeuserid (str | None, optional): 浏览器 Cookies 中的 DedeUserID 字段值. Defaults to None.
            ac_time_value (str | None, optional): 浏览器 Cookies 中的 ac_time_value 字段值. Defaults to None.
        """
        self.sessdata = sessdata
        self.bili_jct = bili_jct
        self.buvid3 = buvid3
        self.dedeuserid = dedeuserid
        self.ac_time_value = ac_time_value

    def get_cookies(self) -> dict:
        """
        获取请求 Cookies 字典

        Returns:
            dict: 请求 Cookies 字典
        """
        return {
            "SESSDATA": self.sessdata,
            "buvid3": self.buvid3 if self.buvid3 else str(uuid.uuid1()) + "infoc",
            "bili_jct": self.bili_jct,
            "DedeUserID": self.dedeuserid,
            "ac_time_value": self.ac_time_value,
        }

    def has_dedeuserid(self) -> bool:
        """
        是否提供 dedeuserid。

        Returns:
            bool。
        """
        return self.dedeuserid is not None

    def has_sessdata(self) -> bool:
        """
        是否提供 sessdata。

        Returns:
            bool。
        """
        return self.sessdata is not None

    def has_bili_jct(self) -> bool:
        """
        是否提供 bili_jct。

        Returns:
            bool。
        """
        return self.bili_jct is not None

    def has_buvid3(self) -> bool:
        """
        是否提供 buvid3

        Returns:
            bool.
        """
        return self.buvid3 is not None
    
    def has_ac_time_value(self) -> bool:
        """
        是否提供 ac_time_value

        Returns:
            bool.
        """
        return self.ac_time_value is not None

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

    def raise_for_no_dedeuserid(self):
        """
        没有提供 DedeUserID 时抛出异常。
        """
        if not self.has_dedeuserid():
            raise CredentialNoDedeUserIDException()
        
    def raise_for_no_ac_time_value(self):
        """
        没有提供 ac_time_value 时抛出异常。
        """
        if not self.has_ac_time_value():
            raise CredentialNoDedeUserIDException()
        
    async def check_valid(self):
        """
        检查 cookies 是否有效

        Returns:
            bool: cookies 是否有效
        """

        data = await get_nav(self)
        return data["isLogin"]

    def generate_buvid3(self):
        """
        生成 buvid3
        """
        self.buvid3 = str(uuid.uuid1()) + "infoc"

    def chcek_refresh(self):
        """
        检查是否需要刷新 cookies

        Returns:
            bool: cookies 是否需要刷新
        """
        return check_cookies(self)

    def refresh(self):
        """
        刷新 cookies
        """
        new_cred: Credential = refresh_cookies(self)
        self.sessdata = new_cred.sessdata
        self.bili_jct = new_cred.bili_jct
        self.dedeuserid = new_cred.dedeuserid
        self.ac_time_value = new_cred.ac_time_value

async def get_nav(credential: Union[Credential, None] = None, headers = None):
    """
    获取导航

    Returns:
        dict: 账号相关信息
    """

    api = API["valid"]
    try:
        cookies = None
        if credential is not None:
            cookies = credential.get_cookies()
        resp = httpx.request("GET", api["url"], cookies=cookies, headers=headers)
    except Exception as e:
        raise e
    return resp.json()["data"]