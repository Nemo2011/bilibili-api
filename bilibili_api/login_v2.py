"""
bilibili_api.login

登录
"""

from dataclasses import dataclass
import json
import threading
import uuid
import base64
import webbrowser
from .utils.network import get_aiohttp_session, get_session
import rsa
import os
from typing import Union, List, Dict
from yarl import URL

from . import settings
from .utils.sync import sync
from .utils.utils import get_api
from .utils.credential import Credential
from .exceptions.LoginError import LoginError
from .utils.network import HEADERS, Api
from .utils.captcha import get_result, close_server, start_server, get_info


API = get_api("login")


def start_geetest_server() -> "ServerThreadModel":
    """
    验证码服务打开服务器

    Returns:
        ServerThread: 服务进程，将自动开启

    返回值内函数及属性:
        (继承：threading.Thread)
        - url   (str)     : 验证码服务地址
        - start (Callable): 开启进程
        - stop  (Callable): 结束进程

    ``` python
    print(start_geetest_server().url)
    ```
    """
    return start_server()  # type: ignore


def close_geetest_server() -> None:
    """
    关闭极验验证服务（打开极验验证服务后务必关闭掉它，否则会卡住）
    """
    return close_server()


def get_geetest_info() -> "GeetestMeta":
    """
    返回极验验证码信息。

    Returns:
        GeetestMeta: 极验验证码信息
    """
    result = get_info()
    return GeetestMeta(
        gt=result["gt"],
        challenge=result["challenge"],
        token=result["token"]
    )


def get_geetest_result() -> Union[None, "GeetestMeta"]:
    """
    返回极验验证码基本&完成信息。

    如果没有完成极验验证码返回 None.

    Returns:
        None | GeetestMeta: 极验验证码信息
    """
    result = get_result()
    if result != -1:
        return GeetestMeta(
            gt=result["gt"],
            token=result["token"],
            challenge=result["challenge"],
            seccode=result["seccode"],
            validate=result["validate"],
        )
    else:
        return None


def encrypt(_hash, key, password) -> str:
    rsa_key = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode("utf-8"))
    data = str(
        base64.b64encode(rsa.encrypt(bytes(_hash + password, "utf-8"), rsa_key)),
        "utf-8",
    )
    return data


async def login_with_password(
    username: str, password: str, geetest: "GeetestMeta"
) -> Union[Credential, "Check"]:
    """
    密码登录。

    Args:
        username (str): 用户手机号、邮箱

        password (str): 密码

        geetest  (GeetestMeta): 极验验证码基本&完成信息 (`get_geetest_result` 获取)

    Returns:
        Union[Credential, Check]: 如果需要验证，会返回 `Check` 类，否则返回 `Credential` 类。
    """
    api_token = API["password"]["get_token"]
    token_data = await Api(**api_token).result
    hash_ = token_data["hash"]
    key = token_data["key"]
    final_password = encrypt(hash_, key, password)
    login_api = API["password"]["login"]
    data = {
        "username": username,
        "password": final_password,
        "keep": True,
        "token": geetest.token,
        "challenge": geetest.challenge,
        "validate": geetest.validate,
        "seccode": geetest.seccode,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://passport.bilibili.com/login",
    }
    sess = (
        get_session()
        if settings.http_client == settings.HTTPClient.HTTPX
        else get_aiohttp_session()
    )
    resp = await sess.request(
        "POST",
        login_api["url"],
        data=data,
        headers=headers,
        cookies={"buvid3": str(uuid.uuid1())},
    )
    login_data = json.loads(
        resp.text
        if settings.http_client == settings.HTTPClient.HTTPX
        else await resp.text()
    )
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


captcha_id = None


def get_countries_list() -> List[Dict]:
    """
    获取国际地区代码列表

    Returns:
        List[dict]: 地区列表
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/countries_codes.json"),
        encoding="utf8",
    ) as f:
        codes_list = json.loads(f.read())
    countries = []
    for country in codes_list:
        name = country["cname"]
        id_ = country["country_id"]
        code = country["id"]
        countries.append({"name": name, "id": code, "code": int(id_)})
    return countries


def search_countries(keyword: str) -> List[Dict]:
    """
    搜索一个地区及其国际地区代码

    Args:
        keyword (str): 关键词

    Returns:
        List[dict]: 地区列表
    """
    list_ = get_countries_list()
    countries = []
    for country in list_:
        if keyword in country["name"] or keyword.lstrip("+") in country["code"]:
            countries.append(country)
    return countries


def have_country(keyword: str) -> bool:
    """
    是否有地区

    Args:
        keyword (str): 关键词

    Returns:
        bool: 是否存在
    """
    list_ = get_countries_list()
    for country in list_:
        if country["name"] == keyword:
            return True
    return False


def have_code(code: Union[str, int]) -> bool:
    """
    是否存在地区代码

    Args:
        code(Union[str, int]): 代码

    Returns:
        bool: 是否存在
    """
    list_ = get_countries_list()
    if isinstance(code, str):
        code = code.lstrip("+")
        try:
            int_code = int(code)
        except ValueError:
            raise ValueError("地区代码参数错误")
    elif isinstance(code, int):
        int_code = code
    else:
        return False
    for country in list_:
        if country["code"] == int_code:
            return True
    return False


def get_code_by_country(country: str) -> int:
    """
    获取地区对应代码

    Args:
        country(str): 地区名

    Returns:
        int: 对应的代码，没有返回 -1
    """
    list_ = get_countries_list()
    for country_ in list_:
        if country_["name"] == country:
            return country_["code"]
    return -1


def get_id_by_code(code: int) -> int:
    """
    获取地区码对应的地区 id

    Args:
        code(int): 地区吗

    Returns:
        int: 对应的代码，没有返回 -1
    """
    list_ = get_countries_list()
    for country_ in list_:
        if country_["code"] == code:
            return country_["id"]
    return -1


class PhoneNumber:
    """
    手机号类
    """

    def __init__(self, number: str, country: Union[str, int] = "+86"):
        """
        Args:
            number(str): 手机号

            country(str): 地区/地区码，如 +86
        """
        number = number.replace("-", "")
        if not have_country(country):  # type: ignore
            if not have_code(country):
                raise ValueError("地区代码或地区名错误")
            else:
                code = country if isinstance(country, int) else int(country.lstrip("+"))
        else:
            code = get_code_by_country(country)  # type: ignore
        self.number = number
        self.code = code
        self.id_ = get_id_by_code(self.code)

    def __str__(self):
        return f"+{self.code} {self.number} (bilibili 地区 id {self.id_})"


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


class ServerThreadModel(threading.Thread):
    """
    A simple model for bilibili_api.utils.captcha._start_server.ServerThread.
    """

    """
    验证码服务链接
    """
    url: str

    def __init__(self, *args, **kwargs): ...

    def stop(self):
        """Stop the server and this thread nicely"""


@dataclass
class GeetestMeta:
    """
    极验验证码完成信息

    NOTE: `gt`, `challenge`, `token` 为验证码基本字段。`seccode`, `validate` 为完成验证码后可得字段。
    """

    gt: str
    challenge: str
    token: str
    seccode: str = ""
    validate: str = ""
