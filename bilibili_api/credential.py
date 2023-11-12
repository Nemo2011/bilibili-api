"""
from bilibili_api import Credential

凭据操作类
"""

import re
import time
import uuid
import binascii
from typing import Union

from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

from .utils.credential import Credential as _Credential
from .utils.network import Api, get_api, get_session, HEADERS

key = RSA.importKey(
    """\
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLgd2OAkcGVtoE3ThUREbio0Eg
Uc/prcajMKXvkCKFCWhJYJcLkcM2DKKcSeFpD/j6Boy538YXnR6VhcuUJOhH2x71
nzPjfdTcqMz7djHum0qSZA0AyCBDABUqCrfNgCiJ00Ra7GmRj+YCK1NJEuewlb40
JNrRuoEUXpabUzGB8QIDAQAB
-----END PUBLIC KEY-----"""
)

API = get_api("credential")


class Credential(_Credential):
    """
    凭据操作类，用于各种请求操作。
    """

    async def check_refresh(self) -> bool:
        """
        检查是否需要刷新 cookies

        Returns:
            bool: cookies 是否需要刷新
        """
        return await check_cookies(self)

    async def refresh(self) -> None:
        """
        刷新 cookies
        """
        new_cred: Credential = await refresh_cookies(self)
        self.sessdata = new_cred.sessdata
        self.bili_jct = new_cred.bili_jct
        self.dedeuserid = new_cred.dedeuserid
        self.ac_time_value = new_cred.ac_time_value

    async def check_valid(self) -> bool:
        """
        检查 cookies 是否有效

        Returns:
            bool: cookies 是否有效
        """
        data = await Api(
            credential=self, **get_api("credential")["info"]["valid"]
        ).result
        return data["isLogin"]


"""
Cookies 刷新相关

感谢 bilibili-API-collect 提供的刷新 Cookies 的思路

https://socialsisteryi.github.io/bilibili-API-collect/docs/login/cookie_refresh.html
"""


async def check_cookies(credential: Credential) -> bool:
    """
    检查是否需要刷新 Cookies

    Args:
        credential (Credential): 用户凭证

    Return:
        bool: 是否需要刷新 Cookies
    """
    api = API["info"]["check_cookies"]
    return (await Api(**api, credential=credential).result)["refresh"]


def getCorrespondPath() -> str:
    """
    根据时间生成 CorrespondPath

    Return:
        str: CorrespondPath
    """
    ts = round(time.time() * 1000)
    cipher = PKCS1_OAEP.new(key, SHA256)
    encrypted = cipher.encrypt(f"refresh_{ts}".encode())
    return binascii.b2a_hex(encrypted).decode()


async def get_refresh_csrf(credential: Credential) -> str:
    """
    获取刷新 Cookies 的 csrf

    Return:
        str: csrf
    """
    correspond_path = getCorrespondPath()
    api = API["operate"]["get_refresh_csrf"]
    cookies = credential.get_cookies()
    cookies["buvid3"] = str(uuid.uuid1())
    cookies["Domain"] = ".bilibili.com"
    resp = await get_session().request(
        "GET", api["url"].replace("{correspondPath}", correspond_path), cookies=cookies, headers=HEADERS.copy()
    )
    if resp.status_code == 404:
        raise Exception("correspondPath 过期或错误。")
    elif resp.status_code == 200:
        text = resp.text
        refresh_csrf = re.findall('<div id="1-name">(.+?)</div>', text)[0]
        return refresh_csrf
    elif resp.status_code != 200:
        raise Exception("获取刷新 Cookies 的 csrf 失败。")


async def refresh_cookies(credential: Credential) -> Credential:
    """
    刷新 Cookies

    Args:
        credential (Credential): 用户凭证

    Return:
        Credential: 新的用户凭证
    """
    api = API["operate"]["refresh_cookies"]
    credential.raise_for_no_bili_jct()
    credential.raise_for_no_ac_time_value()
    refresh_csrf = await get_refresh_csrf(credential)
    data = {
        "csrf": credential.bili_jct,
        "refresh_csrf": refresh_csrf,
        "refresh_token": credential.ac_time_value,
        "source": "main_web",
    }
    cookies = credential.get_cookies()
    cookies["buvid3"] = str(uuid.uuid1())
    cookies["Domain"] = ".bilibili.com"
    resp = await get_session().request("POST", api["url"], cookies=cookies, data=data)
    if resp.status_code != 200 or resp.json()["code"] != 0:
        raise Exception("刷新 Cookies 失败")
    new_credential = Credential(
        sessdata=resp.cookies["SESSDATA"],
        bili_jct=resp.cookies["bili_jct"],
        dedeuserid=resp.cookies["DedeUserID"],
        ac_time_value=resp.json()["data"]["refresh_token"],
    )
    await confirm_refresh(credential, new_credential)
    return new_credential


async def confirm_refresh(
    old_credential: Credential, new_credential: Credential
) -> None:
    """
    让旧的refresh_token对应的 Cookie 失效

    Args:
        old_credential (Credential): 旧的用户凭证

        new_credential (Credential): 新的用户凭证
    """
    api = API["operate"]["confirm_refresh"]
    data = {
        "csrf": new_credential.bili_jct,
        "refresh_token": old_credential.ac_time_value,
    }
    await Api(**api, credential=new_credential).update_data(**data).result
