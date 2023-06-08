"""
bilibili_api.utils.short

一个很简单的处理短链接的模块，主要是读取跳转链接。
"""
import httpx
from .network_httpx import get_session
from .credential import Credential
from .. import settings
from typing import Optional


async def get_real_url(short_url: str, credential: Optional[Credential] = None) -> str:
    """
    获取短链接跳转目标，以进行操作。

    Args:
        short_url(str): 短链接。

        credential(Credential \| None): 凭据类。

    Returns:
        目标链接（如果不是有效的链接会报错）

        返回值为原 url 类型
    """
    credential = credential if credential else Credential()
    config = {}
    config["method"] = "GET"
    config["url"] = short_url
    config["follow_redirects"] = False
    if settings.proxy:
        config["proxies"] = {"all://": settings.proxy}
    try:
        resp = await get_session().head(url=str(short_url), follow_redirects=True)
        u = resp.url
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
