"""
bilibili_api.client

IP 终端相关
"""

from .utils.utils import get_api
from .utils.network import Api

API = get_api("client")


async def get_zone() -> dict:
    """
    通过 IP 获取地理位置

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["zone"]
    return await Api(**api).result


async def get_client_info() -> dict:
    """
    获取 IP 信息

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]
    return await Api(**api).result
