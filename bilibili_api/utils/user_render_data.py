"""
bilibili_api.utils.user_render_data

jwt 渲染数据相关
"""

from re import Pattern, compile
import time
from re import Match, Pattern, compile
from typing import Any

from .network import Credential
from .initial_state import get_initial_state

import jwt

from ..exceptions import ApiException, NetworkException
from .network import HEADERS, Credential, get_client

RENDER_DATA_PATTERN: Pattern[str] = compile(
    r"<script id=\"__RENDER_DATA__\" type=\"application/json\">(.*?)</script>"
)

access_ids = {}
last_timestamp = {}


async def get_webid(url: str, credential: Credential) -> dict[str, Any]:
    """
    获取页面加载静态渲染数据
    """
    if access_ids.get(url) and last_timestamp[url] > int(time.time()):
        return access_ids[url]
    script_render_data = (await get_initial_state(url=url, credential=credential, strict=False))[0]
    if not script_render_data:
        return None
    access_ids[url] = script_render_data["access_id"]
    payload = jwt.decode(jwt=access_ids[url], options={"verify_signature": False})
    created_at: int = payload["iat"]
    ttl: int = payload["ttl"]
    last_timestamp[url] = created_at + ttl
    return access_ids[url]


async def get_user_dynamic_render_data(
    uid: int, credential: Credential
) -> dict[str, Any]:
    """
    获取用户动态页面加载静态渲染数据 获取部分接口需要的 w_webid 关键参数

    :param uid: 用户ID 示例参数: 208259
    :return: 用户动态页面服务端渲染提取数据结构
    """
    return await get_webid(f"https://space.bilibili.com/{uid}/dynamic", credential=credential)
