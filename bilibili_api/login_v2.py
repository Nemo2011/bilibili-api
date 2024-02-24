"""
bilibili_api.login

登录
"""

import json
import uuid
import base64
import webbrowser
from bilibili_api import get_aiohttp_session, get_session
import rsa
from typing import Union
from yarl import URL

from . import settings
from .utils.sync import sync
from .utils.utils import get_api
from .utils.credential import Credential
from .exceptions.LoginError import LoginError
from .utils.network import HEADERS, Api
from .utils.captcha import get_result, close_server, start_server


API = get_api("login")


def encrypt(_hash, key, password) -> str:
    rsa_key = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode("utf-8"))
    data = str(
        base64.b64encode(rsa.encrypt(bytes(_hash + password, "utf-8"), rsa_key)),
        "utf-8",
    )
    return data


def get_geetest() -> object:
    if get_result() != -1:
        return get_result()
    thread = start_server()
    if settings.geetest_auto_open:
        webbrowser.open(thread.url)  # type: ignore
    try:
        while True:
            result = get_result()
            if result != -1:
                close_server()
                return result
    except KeyboardInterrupt:
        close_server()
        exit()


async def login_with_password(
    username: str, password: str
) -> Union[Credential, "Check"]:
    """
    密码登录。

    Args:
        username (str): 用户手机号、邮箱

        password (str): 密码

    Returns:
        Union[Credential, Check]: 如果需要验证，会返回 `Check` 类，否则返回 `Credential` 类。
    """
    api_token = API["password"]["get_token"]
    geetest_data = get_geetest()
    token_data = await Api(**api_token).result
    hash_ = token_data["hash"]
    key = token_data["key"]
    final_password = encrypt(hash_, key, password)
    login_api = API["password"]["login"]
    data = {
        "username": username,
        "password": final_password,
        "keep": True,
        "token": geetest_data["token"],  # type: ignore
        "challenge": geetest_data["challenge"],  # type: ignore
        "validate": geetest_data["validate"],  # type: ignore
        "seccode": geetest_data["seccode"],  # type: ignore
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://passport.bilibili.com/login",
    }
    sess = get_session() if settings.http_client == settings.HTTPClient.HTTPX else get_aiohttp_session()
    resp = await sess.request(
        "POST",
        login_api["url"],
        data=data,
        headers=headers,
        cookies={"buvid3": str(uuid.uuid1())}
    )
    login_data = json.loads(resp.text if settings.http_client == settings.HTTPClient.HTTPX else await resp.text())
    if login_data["code"] == 0:
        if login_data["data"]["status"] == 1:
            return Check(login_data["data"]["url"])
        elif login_data["data"]["status"] == 2:
            raise LoginError("需要手机号进一步验证码验证，请直接通过验证码登录")
        return Credential(
            sessdata=str(resp.cookies.get("SESSDATA")),
            bili_jct=str(resp.cookies.get("bili_jct")),
            dedeuserid=str(resp.cookies.get("DedeUserID")),
            ac_time_value=login_data["data"]["refresh_token"],
        )
    else:
        raise LoginError(login_data["message"])


class Check:
    """
    验证类，如果密码登录需要验证会返回此类

    Attributes:
        check_url (str): 验证 url
        tmp_token (str): 验证 token
    """

    def __init__(self, check_url):
        self.check_url = check_url
        self.yarl_url = URL(self.check_url)
        self.tmp_token = self.yarl_url.query.get("tmp_token")
        self.geetest_result = None
        self.captcha_key = None

    async def fetch_info(self) -> dict:
        """
        获取验证信息

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["safecenter"]["check_info"]
        self.tmp_token = self.check_url.split("?")[1].split("&")[0][10:]
        params = {"tmp_code": self.tmp_token}
        return Api(**api, params=params).result
