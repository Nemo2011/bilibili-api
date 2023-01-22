"""
bilibili_api.utils.short

一个很简单的处理短链接的模块，主要是读取跳转链接。
"""
import httpx
from yarl import URL
from typing import Union
from .network_httpx import get_session
from .. import settings


async def get_real_url(short_url: Union[str, URL]) -> Union[str, URL]:
    """
    获取短链接跳转目标，以进行操作。
    Params:
        short_url(str): 短链接。
    Returns:
        目标链接（如果不是有效的链接会报错）
        返回值为原 url 类型
    """
    config = {}
    config["method"] = "GET"
    config["url"] = short_url
    config["follow_redirects"] = False
    if settings.proxy:
        config["proxies"] = {"all://": settings.proxy}
    try:
        resp = await get_session().head(url=str(short_url), follow_redirects=True)
        u = resp.url # wtf httpx.url
        if type(short_url) == URL:
            return URL(str(u))
        return str(u)
    except Exception as e:
        raise e


async def get_headers(short_url: str) -> httpx.Headers:
    """
    获取链接的 headers。
    """
    config = {}
    config["method"] = "GET"
    config["url"] = short_url
    config["follow_redirects"] = False
    if settings.proxy:
        config["proxies"] = {"all://": settings.proxy}
    resp = await get_session().head(url=short_url, follow_redirects=False)
    return resp.headers
