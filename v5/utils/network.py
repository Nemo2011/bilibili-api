"""
bilibili_api.utils.network

与网络请求相关的模块。能对会话进行管理（复用 TCP 连接）
"""

import aiohttp
from ..exceptions import ApiCodeException, ApiContentTypeException, NetworkException
import json
import re
from .Credential import Credential
from .. import settings

__session: aiohttp.ClientSession = aiohttp.ClientSession()


async def request(method: str, url: str, params: dict = None, data: dict = None,
                  credential: Credential = None, **kwargs):
    """
    向接口发送请求

    :param method: 请求方法
    :param url: 请求 URL
    :param params: 请求参数
    :param data: 请求载荷
    :param credential: Credential 类
    :return: 接口未返回数据时，返回 None，否则返回该接口提供的 data 或 result 字段的数据
    """
    method = method.upper()
    # 请求为非 GET 时要求 bili_jct
    if method != 'GET':
        credential.raise_for_no_bili_jct()

    # 使用 Referer 和 UA 请求头以绕过反爬虫机制
    DEFAULT_HEADERS = {
        "Referer": "https://www.bilibili.com/",
        "User-Agent": "Mozilla/5.0"
    }
    headers = DEFAULT_HEADERS

    if params is None:
        params = {}

    # Session 被关闭时，用于复用 TCP 连接
    global __session
    if __session.closed:
        __session = aiohttp.ClientSession()

    # 自动添加 csrf
    if method in ['POST', 'DELETE', 'PATCH']:
        if data is None:
            data = {}
        data['csrf'] = credential.bili_jct
        data['csrf_token'] = credential.bili_jct

    config = {
        "method": method,
        "url": url,
        "params": params,
        "data": data,
        "headers": headers,
        "cookies": credential.get_cookies()
    }

    config.update(kwargs)

    # 如果用户提供代理则设置代理
    if settings.proxy:
        config["proxy"] = settings.proxy

    resp = await __session.request(**config)

    # 检查状态码
    try:
        resp.raise_for_status()
    except aiohttp.ClientResponseError as e:
        raise NetworkException(e.status, e.message)

    # 检查响应头 Content-Length
    content_length = resp.headers.get("content-length")
    if content_length and int(content_length) == 0:
        return None

    # 检查响应头 Content-Type
    content_type = resp.headers.get("content-type")

    # 响应头不存在该字段
    if content_type is None:
        raise ApiContentTypeException("None")

    # 不是 application/json
    if content_type.lower().index("application/json") == -1:
        raise ApiContentTypeException(content_type)

    raw_data = await resp.text()
    resp_data: dict

    if 'jsonp' in params and 'callback' in params:
        # JSONP 请求
        resp_data = json.loads(re.match("^.*?({.*}).*$", raw_data, re.S).group(1))
    else:
        # JSON
        resp_data = json.loads(raw_data)

    # 检查 code
    code = resp_data.get("code", None)

    if code is None:
        raise ApiCodeException(-1, "API 返回数据未含 code 字段", resp_data)

    if code < 0:
        msg = resp_data.get('msg', None)
        if msg is None:
            msg = resp_data.get('message', None)
        if msg is None:
            msg = "接口未返回错误信息"
        raise ApiCodeException(code, msg, resp_data)

    real_data = resp_data.get("data", None)
    if real_data is None:
        real_data = resp_data.get("result", None)
    return real_data


async def close_session():
    """
    关闭请求 Session，在所有请求完毕后请务必调用这个方法
    :return: None
    """
    if not __session.closed:
        await __session.close()


async def upload_multipart(payload: dict):
    """
    上传 multipart/form-data 类型的数据

    :param payload: 要上传的数据
    """
    pass


def get_session():
    """
    获取当前模块的 aiohttp.ClientSession 对象，用于自定义请求
    """
    return __session
