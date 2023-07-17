"""
bilibili_api.client

IP 终端相关
"""

from .utils.utils import get_api
from .utils.network_httpx import request

API = get_api("client")


async def get_zone() -> dict:
    """
    通过 IP 获取地理位置

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["zone"]
    return await request("GET", api["url"])


async def get_client_info() -> dict:
    """
    获取 IP 信息

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]
    return await request("GET", api["url"])
