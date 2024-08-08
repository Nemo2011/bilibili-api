"""
bilibili_api.login

登录
"""

import json
import uuid
import base64

from .exceptions import GeetestUndoneException
from .utils.network import get_aiohttp_session, get_session, to_form_urlencoded
import rsa
import os
from typing import Union, List, Dict

from . import settings
from .utils.utils import get_api
from .utils.credential import Credential
from .exceptions.LoginError import LoginError
from .utils.network import Api
from .utils.geetest import Geetest


API = get_api("login")


def encrypt(_hash, key, password) -> str:
    rsa_key = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode("utf-8"))
    data = str(
        base64.b64encode(rsa.encrypt(bytes(_hash + password, "utf-8"), rsa_key)),
        "utf-8",
    )
    return data


async def login_with_password(
    username: str, password: str, geetest: Geetest
) -> Credential:
    """
    密码登录。

    Args:
        username (str): 用户手机号、邮箱

        password (str): 密码

        geetest  (Geetest): 极验验证码实例，须完成

    Returns:
        Union[Credential, Check]: 如果需要验证，会返回 `Check` 类，否则返回 `Credential` 类。
    """
    if not geetest.has_done():
        raise GeetestUndoneException()
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
        "token": geetest.key,
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
            raise LoginError("需要手机号进一步验证码验证，请直接通过验证码登录")
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


async def send_sms(phonenumber: PhoneNumber, geetest: Geetest) -> str:
    """
    发送验证码

    Args:
        phonenumber (PhoneNumber): 手机号类
        geetest     (Geetest)    : 极验验证码实例，须完成

    Returns:
        str: captcha_id，需传入 `login_with_sms`
    """
    if not geetest.has_done():
        raise GeetestUndoneException()
    api = API["sms"]["send"]
    data = to_form_urlencoded(
        {
            "source": "main-fe-header",
            "tel": phonenumber.number,
            "cid": phonenumber.code,
            "validate": geetest.validate,
            "token": geetest.key,
            "seccode": geetest.seccode,
            "challenge": geetest.challenge,
        }
    )
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    sess = (
        get_session()
        if settings.http_client == settings.HTTPClient.HTTPX
        else get_aiohttp_session()
    )
    res = await sess.request(
        "POST",
        api["url"],
        data=data,
        headers=headers,
        cookies={"buvid3": str(uuid.uuid1())},
    )
    return_data = res.json()
    if return_data["code"] == 0:
        return return_data["data"]["captcha_key"]
    else:
        raise LoginError(return_data["message"])


async def login_with_sms(
    phonenumber: PhoneNumber, code: str, captcha_id: str
) -> Credential:
    """
    验证码登录

    Args:
        phonenumber (str): 手机号类
        code        (str): 验证码
        captcha_id  (str): captcha_id，为 `send_sms` 调用返回结果

    Returns:
        Credential: 凭据类
    """
    api = API["sms"]["login"]
    data = {
        "tel": phonenumber.number,
        "cid": phonenumber.code,
        "code": code,
        "source": "main_web",
        "captcha_key": captcha_id,
        "keep": "true",
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    sess = (
        get_session()
        if settings.http_client == settings.HTTPClient.HTTPX
        else get_aiohttp_session()
    )
    res = await sess.request(
        "POST",
        api["url"],
        data=data,
        headers=headers,
    )
    return_data = res.json()
    if return_data["code"] == 0 and return_data["data"]["status"] != 5:
        url = return_data["data"]["url"]
        cookies_list = url.split("?")[1].split("&")
        sessdata = ""
        bili_jct = ""
        dede = ""
        for cookie in cookies_list:
            if cookie[:8] == "SESSDATA":
                sessdata = cookie[9:]
            if cookie[:8] == "bili_jct":
                bili_jct = cookie[9:]
            if cookie[:11].upper() == "DEDEUSERID=":
                dede = cookie[11:]
        c = Credential(
            sessdata=sessdata,
            bili_jct=bili_jct,
            dedeuserid=dede,
            ac_time_value=return_data["data"]["refresh_token"],
        )
        return c
    elif return_data["code"] == 0 and return_data["data"]["status"] == 5:
        raise LoginError("需要验证 请使用二维码方式登录")
    else:
        raise LoginError(return_data["message"])
