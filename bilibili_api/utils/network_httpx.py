"""
bilibili_api.utils.network_httpx

重写，使用 httpx
"""

from typing import Any
from urllib.parse import quote
import json
import re
import asyncio
import atexit
import uuid

import httpx

from ..exceptions import ResponseCodeException, ResponseException, NetworkException
from .Credential import Credential
from .. import settings

__session_pool = {}
last_proxy = ""


@atexit.register
def __clean():
    """
    程序退出清理操作。
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        return

    async def __clean_task():
        await __session_pool[loop].close()

    if loop.is_closed():
        loop.run_until_complete(__clean_task())
    else:
        loop.create_task(__clean_task())


async def request(
    method: str,
    url: str,
    params: dict = None,
    data: Any = None,
    credential: Credential = None,
    no_csrf: bool = False,
    json_body: bool = False,
    **kwargs,
):
    """
    向接口发送请求。

    Args:
        method     (str)                 : 请求方法。
        url        (str)                 : 请求 URL。
        params     (dict, optional)      : 请求参数。
        data       (Any, optional)       : 请求载荷。
        credential (Credential, optional): Credential 类。
        no_csrf    (bool, optional)      : 不要自动添加 CSRF。
        json_body  (bool, optional)      : 载荷是否为 JSON

    Returns:
        接口未返回数据时，返回 None，否则返回该接口提供的 data 或 result 字段的数据。
    """
    if credential is None:
        credential = Credential()

    method = method.upper()
    # 请求为非 GET 且 no_csrf 不为 True 时要求 bili_jct
    if method != "GET" and not no_csrf:
        credential.raise_for_no_bili_jct()

    # 使用 Referer 和 UA 请求头以绕过反爬虫机制
    DEFAULT_HEADERS = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0",
    }
    headers = DEFAULT_HEADERS

    if params is None:
        params = {}

    # 自动添加 csrf
    if not no_csrf and method in ["POST", "DELETE", "PATCH"]:
        if data is None:
            data = {}
        data["csrf"] = credential.bili_jct
        data["csrf_token"] = credential.bili_jct

    # jsonp

    if params.get("jsonp", "") == "jsonp":
        params["callback"] = "callback"

    cookies = credential.get_cookies()
    cookies["buvid3"] = str(uuid.uuid1())
    cookies["Domain"] = ".bilibili.com"

    config = {
        "method": method,
        "url": url,
        "params": params,
        "data": data,
        "headers": headers,
        "cookies": cookies,
    }

    config.update(kwargs)

    if json_body:
        config["headers"]["Content-Type"] = "application/json"
        config["data"] = json.dumps(config["data"])

    # config["ssl"] = False

    # config["verify_ssl"] = False
    # config["ssl"] = False

    session = get_session()

    if True:  # try:
        resp = await session.request(**config)
    # except Exception :
    #    raise httpx.ConnectError("连接出错。")

    # 检查响应头 Content-Length
    content_length = resp.headers.get("content-length")
    if content_length and int(content_length) == 0:
        return None

    # 检查响应头 Content-Type
    content_type = resp.headers.get("content-type")

    # 不是 application/json
    if content_type.lower().index("application/json") == -1:
        raise ResponseException("响应不是 application/json 类型")

    raw_data = resp.text
    resp_data: dict

    if "callback" in params:
        # JSONP 请求
        resp_data = json.loads(re.match("^.*?({.*}).*$", raw_data, re.S).group(1))
    else:
        # JSON
        resp_data = json.loads(raw_data)

    # 检查 code
    code = resp_data.get("code", None)

    if code is None:
        raise ResponseCodeException(-1, "API 返回数据未含 code 字段", resp_data)
    if code != 0:
        msg = resp_data.get("msg", None)
        if msg is None:
            msg = resp_data.get("message", None)
        if msg is None:
            msg = "接口未返回错误信息"
        raise ResponseCodeException(code, msg, resp_data)

    real_data = resp_data.get("data", None)
    if real_data is None:
        real_data = resp_data.get("result", None)
    return real_data


def get_session():
    """
    获取当前模块的 httpx.AsyncClient 对象，用于自定义请求

    Returns:
        httpx.AsyncClient
    """
    global __session_pool, last_proxy
    loop = asyncio.get_event_loop()
    session = __session_pool.get(loop, None)
    if session is None or last_proxy != settings.proxy:
        if settings.proxy != "":
            last_proxy = settings.proxy
            proxies = {"all://": settings.proxy}
            session = httpx.AsyncClient(proxies=proxies)
        else:
            last_proxy = ""
            session = httpx.AsyncClient()
        __session_pool[loop] = session

    return session


def set_session(session: httpx.AsyncClient):
    """
    用户手动设置 Session

    Args:
        session (httpx.AsyncClient):  httpx.AsyncClient 实例。
    """
    loop = asyncio.get_event_loop()
    __session_pool[loop] = session


def to_form_urlencoded(data: dict) -> str:
    temp = []
    for [k, v] in data.items():
        temp.append(f'{k}={quote(str(v)).replace("/", "%2F")}')

    return "&".join(temp)
